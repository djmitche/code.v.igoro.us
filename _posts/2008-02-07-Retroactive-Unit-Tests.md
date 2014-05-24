---
layout: post
title:  "Retroactive Unit Tests"
date:   2008-02-07 19:16:00
---


Amanda
 has, for a long time, shipped with an asynchronous communication
library, called event.  It supports the usual suspects: reading and
writing file descriptors, timeouts, and arbitrarily triggerable events.
 It's actually commented a bit better than most of Amanda, but only with
 vaguely suggestive sentences, rather than rigorous descriptions of
behavior.

It has come time to "re-base" this particular library to use glib's [GMainLoop](http://library.gnome.org/devel/glib/unstable/glib-The-Main-Event-Loop.html),
 because other, newer parts of the code will be based on GMainLoop, and
everyone needs to play nice together.  The process is relatively clear:
write thorough unit tests against which the existing implementation
passes, then check the new implementation against those tests.  This
means writing unit tests against existing code that someone else wrote.
 That's hard.

My
initial selection of unit tests gave my new implementation a PASS on the
 first try, so I fired up a backup process, which seemed to work, and
then a recovery, which failed miserably.  Many, many hours of
hand-tracing code later, I uncovered two behaviors of the event library
which were completely undocumented.  I won't make a guess as to whether
they were _intentional and undocumented_ or _unintentional and just happened to work_.  I've now adjusted the comments appropriately, and added unit tests to tickle the funny behavior, but things are still broken.

[EDIT: this sat in my "drafts" folder for no reason]

