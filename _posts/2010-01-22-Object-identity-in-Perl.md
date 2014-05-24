---
layout: post
title:  "Object identity in Perl"
date:   2010-01-22 12:02:00
---


I ran across a surprising weakness in Perl, regarding object identity.  I was writing a function to handle <a>XMsgs</a>,
 which are messages used by the Amanda transfer architecture to indicate
 the progress of a transfer.  Messages sent from any transfer element
are delivered to the same handler, and in this case I needed to know
which element had sent the message.  Fortunately, XMsg objects have a <tt>elt</tt> attribute pointing to the sending element.

Now, in Python, I would write,

def handle_xmsg(xmsg):
    if xmsg.elt is interesting_elt:
      # handle message from interesting_elt
    else:
      # handle message from other elements

where the <tt>is</tt> operator tests for object identity.  So how do I do this in perl?  My first thought was to use <tt>eq</tt>, since the string interpolation of a hashref seems to have an object identifier in it: <tt>HASH(0x711210)</tt>.  I soon learned, in #perl, that <tt>==</tt>
 would work better, as the hashref's address is used as its integer
value, and this conversion is much faster than stringification.

However, the element objects in this particular case are SWIG objects, and furthermore they use <tt>overload</tt> to implement a user-readable stringification.  So neither technique worked.

What I did end up doing was this:

I overrode the <tt>==</tt> operator, and wrote a short comparison function in C to compare the un-SWIGged, un-magicked, un-blessed object pointers.  Whew!

