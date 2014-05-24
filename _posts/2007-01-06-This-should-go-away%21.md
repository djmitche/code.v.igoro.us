---
layout: post
title:  "This should go away!"
date:   2007-01-06 11:25:00
---


One
 of the problems with coding in a high-level language is that sometimes
the insulation from low-level details like memory management is not
complete.  In this post, I present a method for debugging memory leaks
in Python.

## Garbage Collection

Python
 has two kinds of memory management: reference counting and a
mark-and-sweep garbage collector for cycle elimination.  The reference
counting takes care of immediately finalizing objects when the last
reference to them goes away, such as when a variable goes out of scope,
or a key is deleted from a mapping.  This takes care of the vast
majority of objects, but the programmer has to be careful not to create
cycles.  For example, consider this tree implementation:

    class Node:
        def __init__(self, parent=None):
            self.children = []
            self.parent = parent
            if parent: self.parent.children.append(self)

    def make_tree():
        root = Node()
        kid1 = Node(root)
        kid2 = Node(root)
        return root

Now <tt>root</tt>'s <tt>children</tt> references both <tt>kid1</tt> and
<tt>kid2</tt>, but each of those nodes reference <tt>root</tt> via their
<tt>parent</tt> attribute.  This forms a reference cycle (actually two), and
simple reference counting will not finalize it.  For some time now, Python has
had mark-and-sweep garbage collection to periodically seek and destroy these
cycles.  Some time after the last reference to a cycle goes away, the garbage
collection algorithm runs, identifies the cycle as garbage, and finalizes the
objects in the cycle.

## Leaks

Even with full garbage collection, it's still easy to "leak" memory in Python:

*   If large objects are involved in a cycle, they may "hold" theirmemory a lot longer than you'd like, leading to a 2-3x increase inmemory consumption, depending on usage patterns.

*   References can get "stuck" in unexpected places, such as <tt>sys.exc_info</tt>, <tt>threading.Thread</tt> instances, or function closures.

*   If an object in a cycle has a finalizer (<tt>__del__</tt>), the garbage-collection algorithm cannot finalize it, and the entire cycle will persist.

## Leak-Hunting

In the process of chasing what turned out to be several leaks in a large, long-running daemon, I developed a tool I'm calling _shouldGoAway_.  The idea is that the application being debugged calls <tt>shouldGoAway(obj)</tt> when it expects <tt>obj</tt> to go away soon.  The tool makes a weak reference to the object and waits one second.  If the object still exists, it uses the <tt>gc</tt> module to construct a reference graph for the object, and dumps that graph to disk in a format readable by [GraphViz](http://www.graphviz.org/).  Here's how it might be used:

    def compute():
        data_structure = get_data()
        process_data(data_structure)
        shouldGoAway(data_structure, "data_structure")

The tool itself is [shouldGoAway.py](/files/shouldGoAway.py).

### Improvements

*   This module creates a separate <tt>Timer</tt> for every call whichcan lead to a lot of resource consumption if lots of objects should begoing away.  It would probably be sensible to switch to a single threadthat processes objects sequentially.

*   It would be nice to be able to adjust the delay before an object is checked.

*   I think I've struck a nice balance of brevity and useful information in the graph, but there's room for improvement.

*   Many objects (C types, tuples, lists, etc.) are not weak referencable.  It might be nice to work around this.

