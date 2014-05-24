---
layout: post
title:  "Nagios NSCA from Python"
date:   2011-05-20 17:55:00
---


I've
 been working on improving the monitoring of the build slaves at
Mozilla.  As part of this project, I needed to be able to submit passive
 check results to the Nagios servers via [NSCA](http://community.nagios.org/2009/06/11/nagios-setting-up-the-nsca-addon-for-passive-checks/)
 during system startup.  I'm doing this from a Python script that needs
to run on a wide array of systems using whatever random Python is
available.  We run some oddball stuff, so the common denominator is
Python 2.4.

It turns out that there's no Python NSCA library, although there is [Net::Nsca](http://search.cpan.org/dist/Net-Nsca/lib/Net/Nsca.pm) in Perl.  So, I wrote one, and put it on github: [https://github.com/djmitche/pynsca](https://github.com/djmitche/pynsca).

At
the moment, this only knows XOR, and only does service checks.  That's
all I need, but hopefully it can be easily expanded to cover other
purposes.  The one thing I want to avoid is adding mandatory
requirements -- this should work, at least in plain-text and XOR modes,
on a plain-vanilla Python installation.

By the way, the startup script I'm working on is [runslave.py](http://hg.mozilla.org/build/puppet-manifests/file/tip/modules/buildslave/files/runslave.py), which includes a modified copy of _pynsca_ and does a number of other housekeeping jobs as well.  More on that in a subsequent post.

