---
layout: post
title:  "Setting up a buildslave instance remotely on OS X Lion"
date:   2012-03-17 19:05:00
---


Byrce Lelbach has generously offered access to an OS X system as a [metabuildbot](http://buildbot.net/metabuildbot)
 slave.  As I went about setting it up today, the process was not
obvious, so I thought I'd share.  This was interesting mostly because I
only have SSH access to the host, so I cannot download things from the
Apple Store or do any of the fancy point-and-click stuff that would make
 this easier.

First,
 I needed to get XCode installed.  Note that the (much quicker to
download) XCode command-line tools are not sufficient to build
everything in MacPorts -- in particular, they do not support building
zlib, which is required for git-core.

I got my hands on a copy of "Install XCode.app", and:

    host:Downloads buildbot$ cd Install\ Xcode.app/Contents/
    host:Contents buildbot$ sudo installer -package Resources/Xcode.mpkg -target /
    Password:
    installer: Package name is Xcode
    installer: Upgrading at base path /
    installer: The upgrade was successful.

Once this was done, I installed MacPorts:

    host:Downloads buildbot$ hdiutil mount MacPorts-2.0.4-10.7-Lion.dmg
    Checksumming Driver Descriptor Map (DDM : 0)…
        Driver Descriptor Map (DDM : 0): verified   CRC32 $A913D2D8
    Checksumming Apple (Apple_partition_map : 1)…
    ....
        Apple (Apple_partition_map : 1): verified   CRC32 $A1DF5DC1
    Checksumming disk image (Apple_HFS : 2)…
    ...... (...) .....
            disk image (Apple_HFS : 2): verified   CRC32 $5A3E74A0
    Checksumming  (Apple_Free : 3)…
                        (Apple_Free : 3): verified   CRC32 $00000000
    verified   CRC32 $D9641854
    /dev/disk2              Apple_partition_scheme
    /dev/disk2s1            Apple_partition_map
    /dev/disk2s2            Apple_HFS                       /Volumes/MacPorts-2.0.4
    host:Downloads buildbot$ pushd /Volumes/MacPorts-2.0.4/
    /Volumes/MacPorts-2.0.4 ~/Downloads
    host:MacPorts-2.0.4 buildbot$ sudo installer -package MacPorts-2.0.4.pkg/ -target /
    Password:
    installer: Package name is MacPorts-2.0.4
    installer: Installing at base path /
    installer: The install was successful.
    host:MacPorts-2.0.4 buildbot$ popd
    host:Downloads buildbot$ hdiutil unmount /Volumes/MacPorts-2.0.4

and we're off to the races.

I added `/opt/local/bin` to my path as suggested, and then followed the normal MacPorts setup process.

Finishing up the buildslave install required installing Git (which manages to pull in unreasonable amounts of other stuff!)

    host:Contents buildbot$ sudo  /opt/local/bin/port install git-core -credential_osxkeychain-doc-pcre-python27

which is required for the source steps, then creating a virtualenv to install buildbot-slave:

    host:~ buildbot$ virtualenv sandbox
    New python executable in sandbox/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    host:~ buildbot$ source sandbox/bin/activate
    (sandbox)host:~ buildbot$ pip install buildbot-slave
    ...

and then create and start a slave:

    (sandbox)host:~ buildbot$ buildslave create-slave buildslave buildbot.buildbot.net:9989 HOSTNAME PASS
    ...
    (sandbox)host:~ buildbot$ buildslave start buildslave
    ...

I then followed the helpful advice [here](http://kb.askmonty.org/en/buildbot-setup-buildbot-setup-for-macosx) to set up a plist that will start the daemon on boot.

