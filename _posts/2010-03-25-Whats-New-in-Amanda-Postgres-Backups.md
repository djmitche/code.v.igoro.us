---
layout: post
title:  "What's New in Amanda: Postgres Backups"
date:   2010-03-25 19:53:00
---


In the second installment a series of posts about recent work on [Amanda](http://amanda.org/).

The
Application API allows Amanda to back up "structured" data -- data that
cannot be handled well by 'dump' or 'tar'.  Most databases fall into
this category, and with the 3.1 release, Amanda ships with <tt>[ampgsql](http://wiki.zmanda.com/man/ampgsql.8.html)</tt>, which supports backing up [Postgres](http://www.postgresql.org/) databases using the software's [point-in-time recovery](http://www.postgresql.org/docs/current/static/continuous-archiving.html) mechanism.

The how-to for this application is [on the Amanda wiki](http://wiki.zmanda.com/index.php/How_To:Use_Amanda_to_Back_Up_PostgreSQL).

## Operation

Postgres, like most "advanced" databases, uses a logging system to
ensure consistency even in the face of (some) hardware failures.  In
essence, it writes every change that it makes to the database to the
logfile _before_
 changing the database itself.  This is similar to the operation of
logging filesystems.  The idea is that, in the face of a failure, you
just replay the log to re-apply any potentially corrupted changes.

Postgres
 calls its log files WAL (write-ahead log) files.  By default, they are
16MB.  Postgres runs a shell command to "archive" each logfile when it
is full.

So there are two things to back up: the data itself, which can be quite large, and the logfiles.  A full backup works like this:

*   Execute <tt>PG_START_BACKUP(ident)</tt> with some unique identifier.
*   Dump the data directory, excluding the active WAL logs.  Note thatthe database is still in operation at this point, so the dumped data,taken alone, will be inconsistent.
*   Execute <tt>PG_STOP_BACKUP()</tt>.  This archives a text file with the suffix <tt>.backup</tt> that indicates which WAL files are needed to make the dumped data consistent again.
*   Dump the required WAL files

An incremental backup, on the other hand, only requires backing up the already-archived WAL files.

A
restore is still a manual operation -- a DBA would usually want to
perform a restore very carefully.  The process is described on the wiki
page linked above, but boils down to restoring the data directory and
the necessary WAL files, then providing postgres with a shell command to
 "pull" the WAL files it wants.  When postgres next starts up, it will
automatically enter recovery mode and replay the WAL files as necessary.

## Quiet Databases

On older Postgres versions, making a full backup of a quiet database is actually impossible.  After <tt>PG_STOP_BACKUP()</tt>
 is invoked, the final WAL file required to reconstruct a consistent
database is still "in progress" and thus not archived yet.  Since the
database is quiet, postgres does not get any closer to archiving that
WAL file, and the database hangs (or, in the case of ampgsql, times
out).

Newer versions of Postgres do the obvious thing: <tt>PG_STOP_BACKUP()</tt> "forces" an early arciving of the current WAL file.

The
best solution for older versions is to make sure transactions are being
committed to the database all the time.  If the database is truly silent
 during the dump (perhaps it is only accessed during working hours),
then this may mean writing garbage rows to a throwaway table:

    CREATE TABLE push_wal AS SELECT * FROM GENERATE_SERIES(1, 500000);
    DROP TABLE push_wal;

Note that using <tt>CREATE TEMPORARY TABLE</tt> will not work, as temporary tables are not written to the WAL file.

As a brief encounter in <tt>#postgres</tt> taught me, another option is to upgrade to a more modern version of Postgres!

## Log Incremental Backups

DBAs
and backup admins generally want to avoid making frequent full backups,
since they're so large.  The usual pattern is to make a full backup and
then dump the archived log files on a nightly basis for a week or two.
As the log files are dumped, they can be deleted from the database
server, saving considerable space.

In
Amanda terms, each of these dumps is an "incremental", and is based on
the previous night's backup.  That means that the dump after the full is
 level 1, the next is level 2, and so on.  Amanda currently supports 99
levels, but this limit is fairly arbitrary and can be increased as
necessary.

The
problem in ampgsql, as implemented, is that it allows Amanda to schedule
 incremental levels however it likes.  Amanda considers a level-_n_ backup to be everything that has changed since the last level-_n-1_ backup.  This works great for GNU tar, but not so well for Postgres.  Consider the following schedule:

<table>
<tbody><tr><th>Monday</th><td>level 0</td></tr>
<tr><th>Tuesday</th><td>level 1</td></tr>
<tr><th>Wednesday</th><td>level 2</td></tr>
<tr><th>Thursday</th><td>level 1</td></tr>
</tbody></table>

The
problem is that the dump on Thursday, as a level 1, needs to capture all
 changes since the previous level 0, on Monday.  That means that it must
 contain all WAL files archived since Monday, so those WAL files must
remain on the database server until Thursday.

The fix to this is to only perform level 0 or level-_n+1_ dumps, where _n_
 is the level of the last dump performed.  In the example above, this
means either a level 0 or level 3 dump on Thursday.  A level 0 is a full
 backup and requires no history.  A level 3 would only contain WAL files
 archived since the level 2 dump on Wednesday, so any WAL files before
that could be deleted from the database server.

[EDIT: replaced "corrupt" with the more accurate "inconsistent"; clarified final example]

