---
layout: post
title:  "IPv6 Configuration"
date:   2010-06-27 17:27:00
---

 supports IPv6 and I should test that support.  It was also a good
chance to re-immerse myself in network configuration, and Hurricane
Electric has a neat [certification process](http://ipv6.he.net/certification)
 to add some motivation. I began by getting local IPv6 connectivity set
up over the HE tunnel, using my Gentoo systems.  This was fairly
straightforward, as the Gentoo net scripts natively support IPv6\.  The
firewall system I use ([Shorewall](http://www.shorewall.net/)) does not support IPv6 directly.  Instead, there's a parallel <tt xml:base="http://code.v.igoro.us/rss.php?version=2.0&all=1">shorewall6</tt>
 package to install.  Aside from the annoyance of setting up two
separate firewalls, this did not cause appreciable difficulties.  With
all of this in place, I was at the "Explorer" level.

The
next task was to set up a working IPv6 desktop.  My home network uses
802.1q VLAN tagging to layer both an external, publicly routable IPv4
network (99.89.149.16/29 on VLAN 20) and an internal, NAT'd IPv4 network
 (172.16.1/24 on VLAN 10).  I wanted to make VLAN 10 a dual-stack
network, rather than invent a new VLAN for my IPv6 network.  Initially, I
 didn't realize that HE uses, in my case, 2001:470:1f10:826::0/64 just
for the tunnel (yes, two addresses out of 2<sup>64</sup> used -- maybe
we'll need IPv8 sooner than we think!).  I assumed that the /64 I was
allocated was to be used for all of my nodes, and tried to subnet it
locally, using 2001:470:1f10:826::0/112 for the tunnel and
2001:470:1f10::1/112 for the internal network.  This worked with manual
configuration, but [radvd](http://www.litech.org/radvd/)
seemed to always want to advertise a /64\.  A little reading about the RA
 protocol showed this to be correct: RA provides the high 64 bits (the
network portion), and the clients provide the low 64 bits using EUI-64\.
 I was stymied until I looked at the tunnel details again and noticed
that the "Routed IPv6 Prefixes" section listed a different prefix
(2001:470:1f11:826/64).

With
this in place, the subnet and firewall setup was a breeze.  Using a
manual configuration on my MacBook, I was able to communicate via IPv6\.
 However, the stateless autoconfiguration didn't work.  I briefly tried
DHCPv6, but Macs do not support it.  The RA client correctly combines
the network and EUI-64 components to create a full address, and it
correctly copies the link-local address of the router, but it does not
set up a default route using that router, making the whole thing fairly
useless.  A trip to #ipv6 confirmed that Macs are, indeed, broken this
way, so I stopped worrying about it.

The
remainder of the certification process involved getting Apache, Postfix,
 and Bind speaking IPv6, none of which was very difficult.  I did
discover that BIND's $ORIGIN didn't work correctly.  A zonefile with

    $ORIGIN 6.2.8.0.1.1.f.1.0.7.4.0.1.0.0.2.ip6.arpa.
    8.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0 IN PTR knuth.r.igoro.us.

didn't
 work, but spelling out the entire reversed address did.  I'm sure this
was due to a typo, but several checks didn't reveal anything.

However, I'm now stuck at the Guru level until GoDaddy starts supporting IPv6 glue for the <tt>.us</tt> TLD.  I feel cheated, somehow!

