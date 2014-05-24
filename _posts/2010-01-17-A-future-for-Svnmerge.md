---
layout: post
title:  "A future for Svnmerge?"
date:   2010-01-17 15:34:00
---


Svnmerge has always been the kid brother of Subversion.  It's in the project's [contrib](http://svn.apache.org/viewvc/subversion/trunk/contrib/client-side/svnmerge/)
 directory, and is thus unversioned.  Since it's a single Python script,
 users just download it directly from the repository.  In the last year,
 the script has only seen a few non-trivial commits, and the [mailing list](http://www.orcaware.com/mailman/listinfo/svnmerge) has been almost silent.

There
 are some simple reasons for decline.  First, Subversion itself, in
version 1.5, has adopted some of the functionality of Svnmerge.  In
particular, svn now uses properties (<tt>svn:mergeinfo</tt>) to track
the revisions that have and have not been merged into a particular
branch.  There are some limitations, of course.  Most obviously, a
branch can only be "reintegrated" into trunk once, which is not the
workflow of many Svnmerge users.  Also, to my knowledge, Subversion
cannot merge between repositories, while Svnmerge can.

Second,
 Git, Mercurial, and other DVCS's now provide strong support for
merge-heavy workflows.  Both tools also have excellent "gateways" to
Subversion.  For example, Amanda's [Github repository](http://github.com/zmanda/amanda/) tracks the [Subversion repository](http://amanda.svn.sourceforge.net/viewvc/amanda/) using some simple shell scripts.

Between
 these two forces, I think that much of the audience for Svnmerge has
disappeared.  Those left, sadly, will see even less support.

