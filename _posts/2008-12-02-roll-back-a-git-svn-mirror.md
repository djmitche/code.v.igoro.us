---
layout: post
title:  "roll back a git-svn mirror"
date:   2008-12-02 11:15:00
---


Several [Amanda](http://amanda.org/)
 developers use git internally, but the Amanda source code is in
Subversion at SourceForge.  Git-svn manages bidirectional mirroring for
us, and works flawlessly.

Recently,
 however, we introduced a problem through user error: due to a typo in
our git-authors file, a bunch of revisions were mirrored with incorrect
author information.  This was more than a cosmetic problem because it
caused the SHA1 hashes to differ between developers who fixed the typo
at different times (because the author information is included in the
data that feeds the hash algorithm).  This would leave us with divergent
 commits forever.

The
challenge, then, is to make git-svn think that it never fetched that
revision.  HEAD was at r1413, but r1391 had the bad author.  We branched
 for release right after the bum commit, so there are two branches to
deal with.  Here's what I did:

First, roll back the remote branches (e945b67d78c239b42cb882e5c28e24354d0c05f0 is r1390)

    $ git update-ref -m "roll back git-svn" ext/trunk e945b67d78c239b42cb882e5c28e24354d0c05f0
    $ git update-ref -m "roll back git-svn" -d ext/amanda-261 cad126843a7649ca3e05088dd46ee41d7f17e7e2

Next, edit both maxRev values in git-svn's metadata (<tt>.git/svn/.metadata</tt>):

    [svn-remote "ext"]
        reposRoot = https://amanda.svn.sourceforge.net/svnroot/amanda
        uuid = a8d146d6-cc15-0410-8900-af154a0219e0
        branches-maxRev = 1413
        tags-maxRev = 1413

Finally, delete the ._ref_log

    $ rm .git/svn/ext/trunk/.rev_map*
    $ rm .git/svn/ext/amanda-261/.rev_map*

Then just re-run the fetch:

    $ git svn fetch ext

