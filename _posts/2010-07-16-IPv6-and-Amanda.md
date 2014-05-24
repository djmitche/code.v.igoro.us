---
layout: post
title:  "IPv6 and Amanda"
date:   2010-07-16 23:04:00
---


Amanda
 joined the IPv6 revolution in November 2006 - all of the BSD-style
authentication mechanisms can support IPv6 endpoints.  However, it's
generally agreed that this was a mistake, and in this post I will talk
about why that's the case. First, a bit of background on how Amanda's
networking code works, and what had to change to support IPv6\.  Amanda
supports security mechanisms called BSD (the oldest), BSDUDP, and
BSDTCP.  These all authenticate (if you can call it that) using the same
 sorts of checks that rsh uses.  The incoming connection is accepted if:

*   it is from a "reserved" port (less than 1024);
*   the address of the initiator has complementary forward and reverse DNS records in place; and
*   the initiator's hostname is in <tt>.amandahosts</tt>

During a backup operation, the Amanda server contacts each client host.  When using the BSD authentications, this triggers <tt>amandad</tt>,
 which checks the above restrictions before beginning communication with
 the server.  This initial connection is packet-based, and can be
carried out over UDP (for BSD and BSDUDP) or TCP (BSDTCP).  When a dump
begins, several "streams" are opened to transmit the data, index, and
metadata.  For BSD and BSDUDP, each stream is implemented as a distinct
TCP connection, where the client sends a port number to the server and
the server connects to that port.  BSDTCP multiplexes all streams over a
 single TCP connection using a basic type/length packet encapsulation.

The
first challenge in adding IPv6 support was to deal properly with IPv6
addresses when querying the DNS.  That meant switching to getaddrinfo
and getnameinfo, as suggested by [Jun-ichiro itojun Itoh](http://www.kame.net/newsletter/19980604/). These functions bring their own compatibility problems, but Amanda uses [gnulib](http://www.gnu.org/software/gnulib/), which provides compatibile implementations on systems where they are not available, minimizing the difficulty.

We
had a lot of trouble from systems such as RHEL3 possessing IPv6 support
in the compiler environment but not in the kernel.  On such systems,
code using constants like AF_INET6 or AI_V4MAPPED would compile without
problems, but fail at runtime.  We added a WORKING_IPV6 preprocessor
conditional, without which all references to IPv6-related symbols were
removed.  At configure time, Amanda tries to create an IPv6 socket, and
sets this conditional to true if it succeeds.  The <tt>--without-ipv6</tt> configure option forcibly disables IPv6 support.

The
sockaddr structures and API for IPv6 are fairly difficult to use,
particularly if it's not known in advance what sort of address they will
 contain.  We added a set of macros and utility functions in [sockaddr-util.c](http://github.com/zmanda/amanda/blob/master/common-src/sockaddr-util.c) and [sockaddr-util.h](http://github.com/zmanda/amanda/blob/master/common-src/sockaddr-util.h).
  Using these macros throughout Amanda removed a significant amount of
code that was conditionalized on both compile-time support and runtime
address family, and centralized that logic in one easily-maintained
place.

On
our build systems, we had to deal with different levels of support in
the compile environment and the kernel.  This is fine: most Amanda users
 install binary packages that are produced on roughly the same OS
distribution and version as was used for the build, so the kernel
support is generally the same.  However, a third variable has tripped up
 lots of Amanda users: system configuration.  In particular, several
newer Linux distributions have shipped with <tt>localhost</tt> resolving to ::1 vi <tt>/etc/hosts</tt>,
 but without enough interface configuration to actually utilize a socket
 bound to that address.  Amanda uses localhost sockets for inter-process
 communication, so this misconfiguration causes backup operations to
fail.  The solution is to either finish configuring IPv6 on the host,
remove the reference to ::1 in <tt>/etc/hosts</tt>, or build Amanda with <tt>--without-ipv6</tt>.

I
have not yet heard of an Amanda installation where IPv6 communication is
 in use.  But I have heard from countless IPv4 users whose Amanda
installations have failed due to bad IPv6 support.  At the moment, then,
 I feel that adding IPv6 support to Amanda has been a net negative for
the project.  Although there is doubtless room for improvement, I will
not entertain patches for better IPv6 support, for fear they will
introduce new bugs for our exclusively IPv4 userbase.

Of course, all of this may change as dual-stack networks grow more prevalent and are replaced by pure IPv6 networks!

