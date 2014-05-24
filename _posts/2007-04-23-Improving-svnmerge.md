---
layout: post
title:  "Improving svnmerge"
date:   2007-04-23 19:44:00
---


There's been a lot of writing about svnmerge: Ken Kinder [wrote a nice
introductory article](http://kenkinder.com/svnmerge/) on the topic, and now
there's a [wiki](http://www.orcaware.com/svn/wiki/Svnmerge.py) and even a
[mailing list](http://www.orcaware.com/mailman/listinfo/svnmerge).  Maybe
someday soon it will depart the [contrib/
purgatory](http://svn.collab.net/repos/svn/trunk/contrib/client-side/svnmerge/)!

One unusual use of svnmerge is to "branch" a public subversion repository into
your local repository, to allow local development while still tracking the
public trunk.  This is related to vendor branches, but is more suited to the
case where you'll be submitting changes back to the project, and is
particularly useful if you have commit permission on the public repository.
For me, I was merging from the Python repository
(`http://svn.python.org/projects/python/trunk/`) to my own private
repository (let's call it ` http://svn.v.igoro.us/python/trunk`).

Svnmerge has a few weaknesses, but one that surprised me was this: while
svnmerge can manage changes between different repositories, it _can't_ do so
when the repository-relative path is the same in each branch.  In this case,
the repository-relative path for both is `/python/trunk`, so svnmerge
complains:

    svnmerge: cannot init integration source '/python/trunk'
    It must differ from the repository-relative path of the current directory.

# Getting Under The Hood

To understand why this limitation exists, you need to look at how svnmerge
works its magic.  For each managed branch, svnmerge keeps a list of the
revisions in the source branch that have been merged.  By default, this list is
stored in the property `svnmerge-integrated`, looking like
`/python/trunk:1-54918,54920-54926`.  When merging new changes
(`svnmerge merge`), this property gets updated to reflect the newly
merged revisions.  The problem, in this case, is that the identifier for the
branch does not include any information for the repository: does this property
list revisions in my repository, or in the Python repository?

# The Fix

The solution I found to this problem was to qualify the properties with an
identifier for the repository.  For most repositories, the obvious choice is to
use a full URL, e.g.,
`http://svn.python.org/projects/python/trunk:1-54918,54920-54926`.  For
repositories which might be accesed via different URLs by different people, the
UUID might be a better idea, e.g.,
`uuid://6015fed2-1504-0410-9fe1-9d1591cc4771/python/trunk:1-54918,54920-54926`.
To be general, I introduced the notion of a "location identifier" to specify
the location of a branch.  Currently, there are three location identifier
formats:

*   **path**: the "old way" with a simple repository-relative path
*   **url**: a fully qualified URL for the branch
*   **uuid**: a UUID-based identifier

When initializing a new branch, you can specify one of these formats with the `--location-type` flag:

    $ svnmerge init --location-type uuid http://svn.python.org/projects/python/trunk
    property 'svnmerge-integrated' set on '.'
    $ svn pg svnmerge-integrated .
    uuid://6015fed2-1504-0410-9fe1-9d1591cc4771/python/trunk:1-54928

# The Future

Subversion 1.5 promises to support merge tracking natively.  From what little
I've seen, it does this using a similar technique -- keeping lists of revisions
in properties.  However, the developers are not recommending that folks all
convert to 1.5 immediately -- it looks like it will be a significant change
that needs some serious testing first.  Even if it were stable, most Linux
distros are so slow to upgrade that it's reasonable to assume we'll all be
using 1.3 for a good while.

This patch is in the submission process on the mailing list, but an updated
version of svnmerge.py is available [on this
site](http://code.v.igoro.us/files/svnmerge.py), if you'd like to take it for a
spin.  Any feedback would be appreciated!

