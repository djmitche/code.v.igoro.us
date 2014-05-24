---
layout: post
title:  "Revising the allowForce option"
date:   2010-02-13 16:08:00
---


Buildbot's WebStatus display has, for a long time, had an <tt>allowForce</tt>
 option which controls what kind of mayhem can be wrought via the web
interface.  Historically, this has been a boolean option: either web
users can do everything (force builds and shut down slaves) or nothing.
 [Bug 701](http://buildbot.net/trac/ticket/701) asks that we change that to give more granular access control.

Buildbot
 has an interesting way of separating the status display from the
control functionality.  It has two parallel interface hierarchies,
IStatus and IControl, implementing the necessary methods.  The IStatus
hierarchy is illustrated with the orange bubbles here:

![](/img/status.html)

The IControl hierarchy is similar, although it only goes down to the Build level right now.

When <tt>allowForce</tt> is true, the WebStatus object adapts the buildmaster to the IControl interface and adds a link to the result in its <tt>control</tt>
 attribute.  Forcing a build or shutting down a slave then uses this
object to navigate to the appropriate control object and calls a method
from the corresponding interface.  If the <tt>control</tt> attribute is None, no access is allowed.

This scheme has the advantage that it is difficult to accidentally expose functionality, since when <tt>allowForce</tt>
 is false, the control methods are inaccessible.  However, it has the
disadvantage of not allowing any more granular level of access control.

I [just reworked](http://github.com/djmitche/buildbot/commit/7572c5bdad4a09393b665fff2939e605df58deb1)
 the web status to have a more flexible authorization mechanism, and
while I wasn't able to remove the IControl hierarchy entirely, I was
able to marginalize it to only those code blocks that need to perform
controlled actions, instead of passing control objects all over the
place.

