---
layout: post
title:  "What's New in Amanda: Transfer Architecture"
date:   2010-03-12 15:06:00
---


Amanda's
 primary mission in life is to move large quantities of data around.
Historically, this has been done through a patchwork of methods, each
written separately and with its own quirks.  POSIX pipes, TCP sockets,
shared memory, on-disk cache files -- Amanda's done it all.  But these
multiple implementations were error-prone, difficult to maintain, and
often not the most efficient approach.

In an effort to remedy this, we introduced the [transfer architecture](http://wiki.zmanda.com/index.php/Transfer_Architecture), abbreviated XFA.  This was technically included in Amanda-2.6.1, but was only used by _amvault_.
  In the upcoming Amanda-3.1 release, however, the XFA is central to all
 recovery operations, and is used internally by the taper (the portion
of the backup system that writes to devices).

This post highlights some of the features of the transfer architecture, and some of the improvements we'd like to make.

## Transfers and Elements

A transfer is pretty simple: it moves data from one place to another.
It is built from a list of transfer elements, the first being the data
source and the last the destination.  Any elements in the middle are
filters, and could apply compression or encryption, for example.
Elements are automatically connected to one another using the most
efficient means available.

Transfers operate _asynchronously_,
 meaning that ordinary execution of Amanda continues in parallel to the
movement of data.  When the transfer needs Amanda's attention, it sends a
 message, and Amanda reacts accordingly.

The beauty of this architecture is in the variety of elements that can be connected.

*   Sources
    *   File or socket
    *   DirectTCP Connection
    *   Holding Disk
    *   Spanned dumpfile
    *   Random or repeated patterns (for testing)
*   Filters
    *   In-process compression or encryption (e.g., libgz)
    *   External utilities (e.g., gzip or amgpgcrypt)
*   Destinations
    *   File or socket
    *   DirectTCP Connection
    *   Spanned Dumpfile

The full list is given [in the POD](http://wiki.zmanda.com/pod/Amanda/Xfer.html).

## Benefits

The
advantage of the transfer architecture is that it massively simplifies
the process of transferring data.  Nowhere is this more obvious than in
the splitting and re-joining of dumpfiles.

The _Amanda::Xfer::Recovery::Source_ element, which reads from spanned dumpfiles, cooperates with the _[Clerk](http://wiki.zmanda.com/pod/Amanda/Recovery/Clerk.html)_,
 via transfer messages, to load the proper volumes and seek to the
proper files to recover and entire dumpfile, even if it is distributed
over more than one source volume.  Similarly, _Amanda::Xfer::Taper::Dest_ works with a _[Scribe](http://wiki.zmanda.com/pod/Amanda/Taper/Scribe.html)_ to load volumes and update the catalog while spanning dumpfiles.

So
the Amanda taper is a simple wrapper around a transfer from holding disk
 (FILE-WRITE) or socket (PORT-WRITE) to a spanned dumpfile, using a
scribe.  Similarly, all of the recovery tools use a clerk and a transfer
 to read dumpfiles off the appropriate volumes.  And [amvault](http://wiki.zmanda.com/man/amvault.8.html) combines the two to simultaneously read from one volume and write to another.

## Future

At
this point, the transfer architecture is a reliable abstraction, but it
is not yet terribly efficient.  The advantage of the abstraction,
though, is that as it is made more efficient, all of the components of
Amanda that make use of it will immediately become faster, with no
changes.

There
 are plenty of places in Amanda where the transfer architecture will be
useful, and certainly plenty of work to do to make it faster.  If you're
 interested in helping out, please let me know!

