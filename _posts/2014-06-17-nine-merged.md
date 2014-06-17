---
layout: post
title:  "Buildbot Nine Merged to Master"
date:   2014-06-17 12:00:00
categories: [buildbot,code]
---

<img style="float: right;" alt="Buildbot Nine Logo" src="/img/nut-nine-small.png" />

This morning I merged Buildbot's long-term development branch, [`nine`](http://trac.buildbot.net/wiki/Nine), to `master`, following the release of [Buildbot-0.8.9](https://pypi.python.org/pypi/buildbot/0.8.9).
This merge is a major milestone after several years of work by a dedicated core of hackers.

# About Nine #

Nine represents a refactoring of Buildbot into a consistent, well-defined application composed of loosely coupled components.
The components are linked by a common database backend and a messaging system.
This allows components to be distributed across multiple build masters.
It also allows the rendering of complex web status views to be performed in the browser, rather than on the buildmasters.

To encourage contributions from a wider field of developers, the web application is designed to look like a normal AngularJS application.
Developers familiar with AngularJS, but not with Python, should be able to start hacking on the web application quickly.
The web application is "pluggable", so users who develop their own status displays can package those separately from Buildbot itself.

# Today's Changes #

Until today, work on nine took place on a project branch, out of sight of non-core developers.
Most contributors built their patches against the 0.8.x versions, and those patches were then forward-ported into nine by a core developer.
With all the refactoring that has gone on, this forward-porting has become difficult, so after today, patches based on the old, 0.8.x code will no longer be accepted.

# Cool! Let's Try It! #

Work on the nine branch is still very much underway, so don't be tempted to run the latest revision in production.
However, this is a good time to start providing feedback on how well this version works in a testing environment.
It's best to do this in a virtualenv or on a throwaway virtual machine.

Several important things have changed:

* Buildbot now requires Python-2.6 on the master.
* You must install a third package, [`buildbot-www`](https://pypi.python.org/pypi/buildbot-www), to run the master.
  If you see "could not find buildbot-www; is it installed?", this is why!
* You'll need to make some configuration changes - see [the development release notes](http://docs.buildbot.net/latest/relnotes/index.html).

See [Running Buildbot with VirtualEnv](http://trac.buildbot.net/wiki/RunningBuildbotWithVirtualEnv) for a guide to running Buildbot in a testing environment.

Of course, please bring up any problems you encounter either on the [mailing list](https://lists.sourceforge.net/lists/listinfo/buildbot-devel) or in a [Trac issue](http://trac.buildbot.net/).
I'd especially like to hear about any compatibility difficulties that aren't already covered in the release notes -- it's easy to miss those!

# What Happens to 0.8.x? #

That's really up to you!

If there's interest among the Buildbot users, there's an open opportunity to pick up and continue to maintain the 0.8.x releases in the `eight` branch.
It is up to the person who takes this responsibility to set the parameters for that work:

* Will the branch accept new features or only bug fixes?
* Will the maintainers forward-port patches to master?
* How often will releases occur?
