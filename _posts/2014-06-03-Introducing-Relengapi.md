---
layout: post
title:  "Introducing RelengAPI"
date:   2014-06-16 12:00:00
categories: [mozilla,code]
---

# Data! #`

Mozilla's Release Engineering group provides a lot of information and services to the rest of the organization.
To name just a few instances:
* If you want certain kinds of information about builds, you can consult the [BuildAPI](https://secure.pub.build.mozilla.org/buildapi/).
* For others, there are frequently-generated JSON files in [builddata](https://secure.pub.build.mozilla.org/builddata/).
* Events within the build system are transmitted via [Pulse](http://pulse.mozilla.org/).
* Data and operations around buildslaves are in
  * [SlaveAlloc](https://wiki.mozilla.org/ReleaseEngineering/Applications/Slavealloc),
  * [Slave Health](https://wiki.mozilla.org/ReleaseEngineering/Slave_Health),
  * [slaveapi](http://mozilla-slaveapi.readthedocs.org/en/latest/),
  * SlaveLoan, and 
  * [buildbot-configs](http://mxr.mozilla.org/build/source/buildbot-configs/mozilla/production_config.py).
* Various [reports](https://secure.pub.build.mozilla.org/builddata/reports/) on the build system
* Information on clobbers and space usage by builds is in [Clobberer](https://wiki.mozilla.org/ReleaseEngineering/Applications/Clobberer)
* [tooltool](https://wiki.mozilla.org/ReleaseEngineering/Applications/Tooltool) carries a lot of large binary files
* The state of [Jacuzzis](http://atlee.ca/blog/posts/initial-jacuzzi-results.html)' is stored in a Git repository, updated by crontasks.

Release Engineering at Mozilla -- as, I'm sure, at many organizations -- moves quickly.
That means tools get built when they're needed, quickly become critical to operations, and are then difficult to change.
This works well for solving the problem of the moment, but it leaves a fragmented system, as you can see above.

For folks outside of Release Engineering, this is a scary "[maze of twisty little passages, all alike](http://en.wikipedia.org/wiki/Colossal_Cave_Adventure)".
Building any kind of automation that interfaces with these systems is challenging, at best!
And for folks *inside* release engineering, a chorus of unique systems means it takes a lot of time and headspace to come up to speed on each system.
For example, when slaveapi breaks, the set of people who can fix it quickly is very small.

Although decoupled systems make correlated failure less likely and allow parallel, independent development efforts, in this case a failure of just about any of these systems is tree-closing (for you non-Mozillians, that basically means all work stops organization-wide -- bad).

# Release Engineering as a Service #

In an ideal world, Release Engineering systems would interface with the outside world through a nice, well-documented API.
Think of the Github API, or the APIs for the AWS tools.

Building such an interface will allow release engineering to continue to iterate quickly.
In fact, it may allow the group to move more quickly: much of the friction of building a new feature comes from interfacing with other, existing systems.
If those other systems are all available via the same REST API, then that interface becomes trivial.

Such an interface also encourages supportability and cross-pollination between projects.
Since everything interacts with the API, everyone in release engineering knows how the API works and how it is implemented.
If something goes wrong, there's no frantic search for expertise.

Finally, and best of all, this model multiplies Mozilla's force by enabling other Mozillians to develop tools around release engineering.
There are great ideas out there about analyzing build times over time, automatically bisecting failures, automatically landing patches, diagnosing failing slaves, and more.
Today, many of these are difficult for someone outside of releng to work on.
But with an open API, all of these ideas become self-serve: no need to ask for permission or get a release engineer to work on the project.

So how do we get there?

# Releng API #

About a year ago, some members of Release Engineering met at the releng work-week in Boston to discuss application-development best practices.
We decided on a few languages, tools, and processes that we could agree were "good enough", and where there was an advantage to using the same tools everywhere.
This became the Release Engineering [Development Best Practices](https://wiki.mozilla.org/ReleaseEngineering/Development_Best_Practices) document.

Taking that work a step further, it made sense to build a system that already implements all of those best practices.
That system is the [*Releng API* - your interface to release engineering automation](https://wiki.mozilla.org/ReleaseEngineering/Applications/RelengAPI).

It's a "batteries included" approach both for release engineers and API consumers.
It implements lots of features, using the established best practices, and it implements them once -- no re-inventing the wheel required.
Release engineers building a new feature can focus on the feature itself, with all of the usual concerns around deployment, security, management, and mointoring taken care of.
Consumers can interface with the new feature immediately, since it uess exactly the same interface, flows, authentication, and so on as any other release engineering feature.

Development of the API itself is well underway, mirrored at [Github](https://github.com/mozilla/build-relengapi).
The service is up and running at https://api.pub.build.mozilla.org.

We're already building two substantial new features within the framework: [mapper](https://github.com/petemoore/mapper/) and SlaveLoan, and we have plans to port some existing systems to the API.
We're targetting a 1.0.0 release for the next week or so, after which time we'll follow typical semantic versioning practices around compatibility.

# Get Involved #

We would love help and feedback on many aspects of the project, if you have particluar expertise.
We are by no means experts on web security, API design, or UI design!

I will be writing some more technical entries about particular features of the Releng API over the next few weeks.
If something jumps out at you as obviously wrong (or right!), please get in touch.
