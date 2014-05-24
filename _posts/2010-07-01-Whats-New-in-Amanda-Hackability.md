---
layout: post
title:  "What's New in Amanda: Hackability"
date:   2010-07-01 23:29:00
---


It's been a while since I've posted about recent development in [Amanda](http://amanda.org/), but it's not for lack of interesting topics!

Today
 I want to talk a little bit about Amanda's development.  Historically,
Amanda has always had a small, core group of developers who do the
lion's share of the development work.  There are probably lots of
reasons for this, not least of which is that a backup application isn't
the sexiest project on which to spend your spare time.  But I think
there's a deeper reason, and it has to do with hackability.
 Amanda was originally written in C, which means any changes require the
 full set of developer tools.  For example, just to fix a typo in an
error message, you would need to find the source, configure and compile
it, find and fix the error message, and recompile to test.  Fixing
something more substantial in the highly interdependent Amanda codebase
also requires a deep understanding of many parts of Amanda - from the
obscure configuration interface to the oddly interlinked disklist
structure.  This level of programming skill is not common among Amanda's
 user base (systems administrators), and I can count the people who
understand the disklist structure on one hand.

The
result has been a paltry flow of patches from anyone but the core
hackers.  Furthermore, no entry path has been available by which
newcomers could work their way up to being core developers.  While I
don't want to disparage the work of any of the great programmers who
have written Amanda over the years, it's a shame that there have been so
 few at any time, and I worry about what would happen if the number were
 to reach zero.  So what to do?

# $hackability++

We've
 done a few things to try to make Amanda more hackable.  Probably the
biggest change is to rewrite parts of Amanda in Perl.  I'm asked "why"
quite often, and while we had a lot of reasons, two relate directly to
hackability.  First, more sysadmins know Perl than C, because Perl is
quite often used to build the "glue" that links systems together.
Interestingly, based on many conversations, it seems that Python may
also have been a good choice, as I [suspected when I first proposed the rewrite](http://code.v.igoro.us/archives/12-Perl-vs.-Python.html).  But it's too late now!

Second, and more importantly, Perl code can be hacked in place.  If [amvault](http://wiki.zmanda.com/man/amvault.8.html) isn't acting the way you want it to, just open up <tt>/usr/sbin/amvault</tt>
 and tweak away.  No need to download the source, no need to compile, no
 segmentation faults, just hacking.  When you're done, run a quick <tt>diff</tt> and send the results to amanda-hackers.

Even users who do not know Perl can take advantage of this _in-situ_
 hackability.  Within Amanda's C code, if I want a user to try a patch,
that user must figure out how to download Amanda's source, apply the
patch, configure, compile, and install.  None of those steps are
trivial.  With Perl code, I can often provide a patch that is simple
enough to be applied directly to the installed executables by hand, or
with a simple application of <tt>patch</tt>.  Everyone stays focused on the bug under investigation, and the user's backups are up and running that much more quickly.

# New APIs

As I
mentioned before, historically Amanda's code has been highly
interdependent.  Details of the implementation of the holding disk were
spread over most of the files in the server implementation.  The
dumplevel -987 has a special meaning that is documented nowhere, but
referenced in several source files.  All of this makes new development
difficult, because it's impossible to "slice off" and study a portion of
 Amanda in isolation.

The
solution here is to create abstract interfaces, where new functionality
can be "plugged in" and Amanda can use it without changes.  The Amanda
developers have abused the term "API" for these interfaces, and we now
have quite a few:

*   [Application API](http://wiki.zmanda.com/index.php/Application_API) - an abstraction of backup clients, e.g., [ampgsql](http://code.v.igoro.us/archives/50-Whats-New-in-Amanda-Postgres-Backups.html) for Postgres;
*   [Device API](http://wiki.zmanda.com/index.php/Device_API) - an abstraction of backend storage devices, such as tape, disk, cloud, or DVD-RW;
*   [Changer API](http://wiki.zmanda.com/index.php/Changer_API) - an abstraction of tape changers and other mechanisms for selecting from a set of volumes; and
*   [Script API](http://wiki.zmanda.com/index.php/Script_API) - a means of invoking scripts before or after certain events during a backup.

This
strategy has already paid off: we have seen several new scripts and
applications contributed, and the DVD-RW device arrived out of the blue
as a contribution from someone who found it useful.

# Other Changes

In the interest of greater accessibility to new hackers, we have also put Amanda on [github](http://github.com/zmanda/amanda) and created a set of good "beginner" projects.  Zmanda has even offered to [pay people to hack on Amanda](http://code.v.igoro.us/archives/53-Want-to-work-on-Amanda.html),
 as a way of easing the cost of entry.  I also try to point out
interesting projects on the Amanda mailing list, particularly projects
that Jean-Louis and I probably will not find time to work on.

The
idea here is to encourage new hackers to pick up a well-scoped project
to become familiar with Amanda.  The hackers can then move on to more
sophisticated projects that meet their particular backup needs or
address a particular interest.

# Will You Join Me?

So Amanda is ready for you.  When can you start?

