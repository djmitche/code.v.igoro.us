"""
Implements a function to check that an object gets cleanly garbage collected,
and to help track down reference cycles if it does not.
"""
import os
import gc
import sys
import types
import weakref
import logging
import threading
import traceback

enabled = False
shouldGoAwayDir='/tmp'

__all__ = [ 'shouldGoAway' ]

def shouldGoAway(object, description=None):
    """
    Caller expects C{object} to go away shortly due to reference-counting
    GC.

    This function begins by delaying slightly, to allow any stack frames
    to complete and release references to this object.  If the object
    does not go away after that delay, the function will dump a graphviz-
    formatted reference graph of the object to the directory specified by
    the global variable C{shouldGoAwayDir).

    If the global variable C{enabled} is False, does nothing.

    @param object: the object that should go away
    @type object: any Python object

    @param description: the kind of object; this is used as a filename
    component, so it should not contain any funny characters.  If not specified,
    the type of C{object} is used.
    @type description: string
    """
    if not enabled or object is None: return

    if not description:
        try: description = type(object).__name__
        except: description = 'unknown'

    # store only a weak reference to the object
    objref = weakref.ref(object)

    # and call shouldBeGone(objref, description) in a little bit
    # (1s seems adequate, even under high load)
    t = threading.Timer(1.0, shouldBeGone, [ objref, description ])
    t.setDaemon(1)
    t.start()


####
# Internal functions

def format_description(o):
    """
    Format a (potentially very long) description of C{o} as a string.
    """
    if isinstance(o, types.FrameType):
        return "<<frame " + (" ".join(map(str,
                [o.f_code,
                 o.f_locals.keys(),
                 o.f_globals["__name__"],
                 o.f_globals.get('__file__', '?'),
                 o.f_lineno]))) + ">>"
    else:
        return repr(o)

def format_label(o):
    """
    Format a (very short) label for C{o} -- one or two words to identify the object.
    """
    try:
        label = type(o)
        label = label.__name__
    except:
        label = 'unknown object'

    # try to be a bit more descriptive where possible
    if label == 'instance':
        try: label = o.__class__.__name__ + ' instance'
        except: pass
    elif label == 'module':
        try: label = "module '%s'" % o.__name__
        except: pass
    elif label == 'frame':
        try: label = "frame for '%s'" % o.f_code.co_name
        except: pass

    return label

def should_recurse(o):
    """
    Do we want to explore references to the given object?
    """
    if o is None: return False # should be impossible..
    if o in sys.modules.values(): return False # relatively terminal
    return True

def getReferenceGraph(obj, max_depth, *ignore_these):
    """
    Generate a reference graph for C{obj} to the specified maximum depth

    The results contain no references to existing objects, and consist entirely
    of strings and integer object identifiers.  The returned C{links} is a list of
    pairs C{(s,d)}, indicating that the object with id C{s} holds a reference to
    the object with id S{d}.  The returned C{objs} is a dictionary keyed by object
    id, where the values are tuples C{(label, description)} of a short label and
    a longer description.

    @param obj: an object

    @param max_depth: the maximum depth to explore; 10 is a nice choice.

    @param ignore_these: objects which should be ignored completely during the
    graph generation (objects which refer to C{obj} but which are not of interest)

    @returns: tuple C{(links, objs)}
    """
    links = {}
    objs = { id(obj) : (format_label(obj), format_description(obj)) }

    # object_queue is a queue of pairs (obj, depth) of objects yet to be examined
    object_queue = [ (obj, 0) ] 

    # get a list of referrers for a fake object, which will helpfully
    # include the frame for this function; also record the id of whatever
    # objects the caller would like us to ignore
    fake_obj = [ ]
    ignore_ids = [ id(x) for x in gc.get_referrers(fake_obj) ] \
               + [ id(x) for x in ignore_these ]
    del fake_obj
    del ignore_these
    del x

    while object_queue:
        obj, depth = object_queue.pop(0)
        obj_links = []
        for subobj in gc.get_referrers(obj):
            sub_id = id(subobj)

            # ignore this link if it's a reference from this function
            if sub_id in ignore_ids: continue

            # record a link from this object
            obj_links.append(sub_id)

            # have we already seen this object?
            if sub_id in objs: continue

            # record the description of this object
            objs[sub_id] = (format_label(subobj), format_description(subobj))

            # and queue it for later analysis if it's not already queued
            if depth < max_depth and should_recurse(subobj):
                object_queue.append((subobj, depth+1))
        links[id(obj)] = obj_links

    # turn the 'links' dictionary, which contains backward links,
    # into a series of forward-link pairs
    linkpairs = []
    for dst, srcs in links.iteritems():
        for src in srcs:
            linkpairs.append((src, dst))
    return objs, linkpairs

def makeDotFile(start_node, objs, links, description, file):
    print >>file, "digraph referencegraph {"
    print >>file, "  node [ fontsize=8 ];"

    # output links between objects by ID
    for link in links:
        print >>file, "  x%016x -> x%016x;" % link

    # and then the nodes themselves
    for ptr, (label, descr) in objs.items():
        print >>file, ''

        # node descriptions are huge, so they are stored as comments in the .dot file
        print >>file, "  // %s" % descr.replace('\n', '\n  // ')

        # add labels for the nodes, and color the start node red.
        attrs = { 'label' : "\"%s\\n(0x%016x)\"" % (label.replace('"', r'\"'), ptr) }
        if ptr == start_node: attrs['color'] = "red"
        attrstring = ','.join(("%s=%s" % it) for it in attrs.iteritems())
        print >>file, "  x%016x [%s];" % (ptr, attrstring)

    print >>file, "}"

def shouldBeGone(objref, description):
    # we avoid putting the object in question in a local variable, as then
    # our <frame> will reference it; instead, we put it in a tuple and pass that
    # tuple to getReferenceGraph as something it should ignore.
    objref = ( objref(), )
    if objref[0] is None: return # good -- it's already gone

    try:
        # the object is still around -- let's build a graph
        filename = os.path.join(shouldGoAwayDir, '%s-0x%016x.dot' % (description, id(objref[0])))
        file = open(filename, 'w')
        objs, links = getReferenceGraph(objref[0], 10, objref)
        makeDotFile(id(objref[0]), objs, links, description, file)
        file.close()
    except:
        typ, val, tb = sys.exc_info()
        logging.warn("Exception in reference logging: %s %s %s" % (typ, val, tb))
    else:
        logging.warn("%s object did not go away; %d objects logged to '%s'"
                % (description, len(objs), filename))
