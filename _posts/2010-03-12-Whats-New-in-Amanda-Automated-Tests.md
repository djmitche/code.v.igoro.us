---
layout: post
title:  "What's New in Amanda: Automated Tests"
date:   2010-03-12 13:03:00
---


This is the first in what will be a series of posts about recent work on [Amanda](http://amanda.org/).
  Amanda has a reputation as old and crusty -- not so!  Hopefully this
series will help to illustrate some of the new features we've completed,
 and what's coming up.  I'll be cross-posting these on [the Zmanda Team Blog](http://www.zmanda.com/blogs/) too.

![Chart](/img/chart.png)

Among
 open-source applications, Amanda is known for being stable and highly
reliable.  To ensure that Amanda lives up to this reputation, we've
constructed an automated testing framework (using [Buildbot](http://buildbot.net/))
 that runs on every commit.  I'll give some of the technical details
after the jump, but I think the numbers speak for themselves.  The
latest release of Amanda (which will soon be 3.1.0) has 2936 tests!

These
 tests range from highly-focused unit tests, for example to ensure that
all of Amanda's spellings of "true" are parsed correctly, all the way up
 to full integration: runs of amdump and the recovery applications. The
tests are implemented with Perl's <tt>Test::More</tt> and <tt>Test::Harness</tt>.  The result for the [current trunk](http://github.com/zmanda/amanda/commit/deb1d40c203906bd949789c4fab08172d54c49cc) looks like this:

    =setupcache.....................ok
    Amanda_Archive..................ok
    Amanda_Changer..................ok
    Amanda_Changer_compat...........ok
    Amanda_Changer_disk.............ok
    Amanda_Changer_multi............ok
    Amanda_Changer_ndmp.............ok
    Amanda_Changer_null.............ok
    Amanda_Changer_rait.............ok
    Amanda_Changer_robot............ok
    Amanda_Changer_single...........ok
    Amanda_ClientService............ok
    Amanda_Cmdline..................ok
    Amanda_Config...................ok
    Amanda_Curinfo..................ok
    Amanda_DB_Catalog...............ok
    Amanda_Debug....................ok
    Amanda_Device...................ok
            211/428 skipped: various reasons
    Amanda_Disklist.................ok
    Amanda_Feature..................ok
    Amanda_Header...................ok
    Amanda_Holding..................ok
    Amanda_IPC_Binary...............ok
    Amanda_IPC_LineProtocol.........ok
    Amanda_Logfile..................ok
    Amanda_MainLoop.................ok
    Amanda_NDMP.....................ok
    Amanda_Process..................ok
    Amanda_Recovery_Clerk...........ok
    Amanda_Recovery_Planner.........ok
    Amanda_Recovery_Scan............ok
    Amanda_Report...................ok
    Amanda_Tapelist.................ok
    Amanda_Taper_Scan...............ok
    Amanda_Taper_Scan_traditional...ok
    Amanda_Taper_Scribe.............ok
    Amanda_Util.....................ok
    Amanda_Xfer.....................ok
    amadmin.........................ok
    amarchiver......................ok
    amcheck.........................ok
    amcheck-device..................ok
    amcheckdump.....................ok
    amdevcheck......................ok
    amdump..........................ok
    amfetchdump.....................ok
    amgetconf.......................ok
    amgtar..........................ok
    amidxtaped......................ok
    amlabel.........................ok
    ampgsql.........................ok
            40/40 skipped: various reasons
    amraw...........................ok
    amreport........................ok
    amrestore.......................ok
    amrmtape........................ok
    amservice.......................ok
    amstatus........................ok
    amtape..........................ok
    amtapetype......................ok
    bigint..........................ok
    mock_mtx........................ok
    noop............................ok
    pp-scripts......................ok
    taper...........................ok
    All tests successful, 251 subtests skipped.
    Files=64, Tests=2936, 429 wallclock secs (155.44 cusr + 31.48 csys = 186.92 CPU)

The
skips are due to tests that require external resources - tape drives,
database servers, etc.  The first part of the list contains tests for
almost all perl packages in the <tt>Amanda</tt> namespace.  These are
generally unit tests of the new Perl code, although some tests integrate
 several units due to limitations of the interfaces.  The second half of
 the list is tests of Amanda command-line tools.  These are integration
tests, and ensure that all of the documented command-line options are
present and working, and that the tool's behavior is correct.  The
integration tests are necessarily incomplete, as it's simply not
possible to test every permutation of this highly flexible package.

The <tt>=setupcache</tt>
 test at the top is interesting: because most of the Amanda applications
 need some dumps to work against, we "cache" a few completed amdump runs
 using tar, and re-load them as needed during the subsequent tests.
This speeds things up quite a bit, and also removes some variability
from the tests (there are a _lot_ of ways an amdump can go wrong!).

The entire test suite is run at least 54 times for every commit by [Buildbot](http://buildbot.net/).
  We test on 42 different architectures - about a dozen linux distros,
in both 32- and 64-bit varieties, plus Solaris 8 and 10, and
Darwin-8.10.1 on both x86 and PowerPC.  The remaining tests are for
special configurations -- server-only, client-only, special runs on a
system with several tape drives, and so on.

