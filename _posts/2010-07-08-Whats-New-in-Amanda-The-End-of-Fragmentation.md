---
layout: post
title:  "What's New in Amanda: The End of Fragmentation"
date:   2010-07-08 19:07:00
---


Most
 of my posts in this series have been about features that are available
in a released version of Amanda.  This time, I want to share a project
I'm working on right now - one that will be available in Amanda-3.2\.
I'm reworking the way Amanda writes its data to tape (or any other kind
of storage) to make it more efficient, more reliable, and simpler to
configure.

Historically,
 Amanda's conservative approach to finicky tape hardware has meant that
it wasted some space at the end of each tape.  With the changes I'm
working on, Amanda will no longer waste this space, and can also avoid
some needless copying of data in most cases, with a minimum of
additional risk.

# Amanda's Storage Format

Before examining the new functionality, let's look at Amanda's storage format.  Amanda treats all storage devices like tapes<sup>1</sup>
 - a set of sequentially numbered data files of arbitrary size, each
composed of a sequence of fixed-size blocks.  Each file begins with a
one-block header that identifies the dump and gives information about
its contents.  The header is followed by blocks of raw data.

Amanda supports writing a dump across multiple tapes - spanning.<sup>2</sup>
  The technique is this: a dump is split into a sequence of parts, and
each part is written a a single file on a volume.  During recovery,
Amanda reads the parts in sequence, and concatenates their data to
reproduce the original dumpfile.  Usually all parts are the same size,
and this size is generally 1-5% of the tape capacity.

# Better Safe than Sorry - At a Cost

Amanda
 was originally designed around tape drives - in fact, if you look at
the history of Linux kernel support for tape drives, it is closely
intertwined with Amanda development.  Tape drives are finicky beasts,
and in many cases cannot distinguish the end of the tape (called EOM)
from any other fatal error.  Worse, tape drives employ large caches to
ensure they can write continuously, and when an error occurs all of the
data in that cache is lost, and there is no way for Amanda to determine
how much actually made it onto the tape.  Beginning a new on-tape file
(writing a filemark) flushes the cache and signals any errors
immediately.

Since
 time immemorial, then, Amanda has treated any error from the tape drive
 as EOM, and assumed that all data written since the last filemark is
potentially corrupt.  That means that the part in progress when the
error occurred is logged as PARTIAL, and Amanda will start at the
beginning of that part on the next tape.

The
PARTIAL part is recorded in the catalog, but will not be used for
recovery, so it is effectively wasted space.  A little arithmetic will
tell you that, on average, each tape will waste half of the part size.
This is at least excusable with real tape drives; with vtapes (disk),
this wasted space is completely unnecessary.  Worse, vtapes are most
flexible when they are kept small and dumps are spanned over many vtapes
 per night; but the wasted space increases linearly with the number of
vtapes used.

In
order to rewind a part and write it again on a new tape, Amanda also
needs to keep its data somewhere, called the part cache.  When the dump
is on the holding disk, the holding disk acts as a part cache.
Otherwise, Amanda can cache parts in memory or on disk.  Caching in
memory is faster, but requires a lot of RAM for a reasonable part size.
 Caching on disk allows larger parts, but is considerably slower.

# Logical EOM

More
recent tape drives (those made in the last decade or so) have a feature
called "early warning".  With this feature enabled, the drive alerts the
 host system when it is "near" EOM, and flushes the cache to tape.
Exactly what "near" means is not specified in the SCSI standard, but in
general there's room to flush the cache and write a filemark, at least.
 This is sometimes called a logical EOM - LEOM.

Amanda
 can take advantage of this functionality to cleanly finish a part
before running headlong into a physical EOM.  This eliminates the wasted
 space for a PARTIAL part, and also eliminates the need to cache parts,
since rewinding is not required.  In one small change (well, OK, it's [about 4,300 lines](http://github.com/zmanda/amanda/compare/1bc521c5ce1be2d144fefc8ce37917c55ab690e8...6a087798ea0c9945093226150da37d5af49d1810)), Amanda gets faster and uses storage space more efficiently.  What's not to love?

Better
 yet, all of the non-tape devices (vtapes, S3 devices, DVD-ROMs, etc.)
can easily emulate LEOM, so backups to these devices will automatically
benefit from this improvement.

# In the Code

[Three important patches](http://github.com/zmanda/amanda/compare/1bc521c5ce1be2d144fefc8ce37917c55ab690e8...6a087798ea0c9945093226150da37d5af49d1810)
 toward this functionality were just committed.  What remains is to set
up real LEOM support for the VFS device (vtapes) and for the tape
device.

The
VFS device can, of course, trivially emulate LEOM when it is enforcing
the `MAX_VOLUME_USAGE` property - the vtape length.  However, predicting
when a filesystem will run out of space is much more difficult.  We are
still discussing options, and I would love to hear suggestions here or
on the mailing list.

As
for the tape device, it will assume that LEOM is not supported unless
the user configures it explicitly (with the "LEOM" device property) or
we can determine support for LEOM from the operating system at runtime.
 Unfortunately, this is one of those areas so technical that only a
half-dozen people know how it works, so it may take me some time to
track down this information for non-Linux operating systems.  Again,
advice and assistance is welcome!

* * *

*   <sup>1</sup>This is an ages-old design decision, but one that artificially constrains Amanda's flexibility, especially with vtapes.
*   <sup>2</sup>In fact, Amanda has supported spanning forsomething like 7 years now.  Yet I occasionally see users in #amandacomplaining about this serious limitation and wondering when we're going
 to do anything about it.  Will 2003 be soon enough?

