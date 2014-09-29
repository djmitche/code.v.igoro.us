---
layout: post
title:  "fwunit: Unit Tests for your Network"
date:   2014-09-29 12:00:00
categories: [code,mozilla]
---

![I find your lack of unit tests ... disturbing](http://www.quickmeme.com/img/7d/7d50b56276ee0f174b1f708ab7a1c0c29dff5fab0f5363b78404cce3dcb6eed8.jpg "I find your lack of unit tests ... disturbing")

It's established fact by now that code should be tested.  The benefits are many:

  * Exercising the code;
  * Reducing ambiguity by restating the desired behavior (in the implementation, in the tests, and maybe even a third time in the documentation); and
  * Verifying that the desired behavior remains unchanged when the code is refactored.

System administrators are increasingly thinking of infrastructure as code and reaping the benefits of testing, review, version control, collaboration, and so on.
In the networking world, this typically implies "software defined networking" (SDN), a substantial change from the typical approach to network system configuration.

At Mozilla, we haven't taken the SDN plunge yet, although there are plans in the works.
In the interim, we maintain very complex firewall configurations by hand.
Understanding how all of the rules fit together and making manual changes is often difficult and error-prone.
Furthermore, after years of piece-by-piece modifications to our flows, the only comprehensive summary of our network flows are the firewall configurations themselves.
And those are not very readable for anyone not familiar with firewalls!

The difficulty and errors come from the gap between the request for a flow and the final implementation, perhaps made across several firewalls.
If everyone -- requester and requestee -- had access to a single, readable document specifying what the flows *should* look like, then requesets for modification could be more explicit and easier to translate into configuration.
If we have a way to verify automatically that the firewall configurations match the document, then we can catch errors early, too.

I set about trying to find a way to implement this.
After experimenting with various ways to write down flow definitions and parse them, I realized that the verification tests could *be* the flow document.
The idea is to write a set of tests, in Python since it's the lingua franca of Mozilla, which can be read by both the firewall experts and the users requesting a change to the flows.
To change flows, change the tests -- a diff makes the request unambiguous.
To verify the result, just run the tests.

fwunit
------

I designed [fwunit](https://github.com/mozilla/build-fwunit) to support this: unit tests for flows.
The idea is to pull in "live" flow configurations and then write tests that verify properties of those configurations.
The tool supports reading Juniper SRX configurations as well as Amazon AWS security groups for EC2 instances, and can be extended easily.
It can combine rules from several sources (for example, firewalls for each datacenter and several AWS VPCs) using a simple description of the network topology.

As a simple example, here's a test to make sure that the appropriate VLANs have access to the [DeployStudio](http://deploystudio.com/Home.html) servers:

    def test_install_build():
        rules.assertPermits(
            test_releng_scl3 + try_releng_scl3 + build_releng_scl3,
            deploystudio_servers,
            'deploystudio')

The ``rules`` instance there is a compact representation of all allowed network flows, deduced from firewall and AWS configurations with the ``fwunit`` command line tool.
The ``assertPermits`` method asserts that the rules permit traffic from the test, try, and build VLANs to the deploystudio servers, using the "deploystudio" application.
That all reads pretty naturally from the Python code.

At Mozilla
----------

We glue the whole thing together with a shell script that pulls the tests from our private git repository, runs ``fwunit`` to get the latest configuration information, and then runs the tests.
Any failures are reported by email, at which point we know that our document (the tests) doesn't match reality, and can take appropriate action.

We're still working on the details of the process involved in changing configurations -- do we update the tests first, or the configuration?
Who is responsible for writing or modifying the tests -- the requester, or the person making the configuration change?
Whatever we decide, it needs to maximize the benefits without placing undue load on any of the busy people involved in changing network flows.

Benefits
--------

It's early days, but this approach has already paid off handsomely.

  * As expected, it's a readable, authoritative, verifiable account of our network configuration.  Requirements met -- aweseome!
  * With all tests in place, netops can easily "refactor" the configurations, using fwunit to verify that no expected behavior has changed.
    We've deferred a lot of minor cleanups as high-risk with low reward; easy verification should substantially reduce that risk.
  * Just about every test I've written has revealed some subtle misconfiguration -- either a flow that was requested incorrectly, or one that was configured incorrectly.
    These turn into flow-request bugs that can be dealt with at a "normal" pace, rather than the mad race to debug and fix that would occur later, when they impacted production operations.

Get Involved
------------

I'm a Mozillan, so naturally fwunit is open source and designed to be useful to more than just Mozilla.
If this sounds useful, please use it, and I'd love to hear from you about how I might make it work better for you.
If you're interested in hacking on the software, there are a number of open issues in the [github repo](https://github.com/mozilla/build-fwunit/issues) just waiting for a pull request.
