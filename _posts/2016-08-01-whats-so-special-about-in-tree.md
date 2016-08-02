---
layout: post
title:  "What's So Special About \"In-Tree?\""
date:   2016-08-03 17:43:00
categories: [mozilla]
---

The TaskCluster team uses the phrase "in-tree" all the time: in-tree docker images, in-tree task configuration, in-tree scheduling, ..
So, what's the big deal?
Why are we so excited?

## What Does It Mean?

TaskCluster's primary purpose is as the continuous integration system for Firefox.
While the TaskCluster platform's applicability is much larger, Firefox is the organization's bread and butter, so that's where we are focused.
The Firefox source code is all in a single directory tree of source code, the "[gecko tree](https://hg.mozilla.org/mozilla-central)".
So when we refer to functionality being "in-tree', we mean that it is implemented in that directory tree.

## Why Does It Matter?

Historically, lots of functionality has been implemented outside the gecko tree: Mozharness was in a separate repository until about a year ago, and Buildbot functionality spans four non-gecko repositories.
[PuppetAgain ](https://wiki.mozilla.org/ReleaseEngineering/PuppetAgain), the tool that controls what is installed and running on all release engineering workers and servers, is in its own repository, too.

This leads to some deep and frustrating issues.
In general, it's very difficult to coordinate changes across multiple repositories.
For example, consider upgrading the version of a library on test workers.
The upgrade itself needs to be performed in the PuppetAgain repository, and will take about 36 hours to fully "propagate" as machines finish their work and check in with the puppet servers.
During this time, some machines have the old version, and some have the new, leading to great confusion if the difference causes job failures.
Only after the change has completely propagated can developers land a change in the gecko tree to utilize the new library.
But even that is fraught with difficulty: there are many copies (branches) of the gecko source, ranging from try and integration branches which change quickly and break often, through mozilla-central (nightly), aurora, beta, release, and ESR.
It is risky, and requires special permission, to land patches on branches later in that list.
And if anything goes wrong, backing out all of these changes is difficult and might take another few days, during which time things are broken and people aren't able to get their work done.

We've worked around issues like this in a number of ways -- none of them good.
In this case, we might install both versions of the library on every machine, including some switch in-tree indicating which library version to use.
Once everything is switched over, we can remove the old version from the machines.
However, it can take a year for an ESR branch to be removed, by which time we have hundreds of changes we need to remove, with corresponding risk and complexity.

Configuration that isn't in-tree is also difficult for Firefox developers to modify.
For example, neither PuppetAgain nor Buildbot have any good facilities for experimenting with a change before deploying it (they have *some* facilities, but they aren't great or easy to use).
In practice, given the high risk and specialized knowledge required, most changes to these systems are made by filing a bug for someone else to do the work.
That "someone else" might be busy or away on vacation or just not awake during the developer's working day, in which case the change gets delayed.

In short, out-of-tree changes have caused a lot of friction and slowness in our development process.

## What's the New Plan?

One of the design goals of TaskCluster is to make CI infrastructure changes "self-serve".
That means that a Firefox developer who wants to change something about how CI works can make that change herself, without asking permission or requiring someone else's expertise.
Based on previous experience, we have a pretty good idea of what kinds of changes are most popular:

 * adding new job types or tweaking existing jobs with a new configuration parameter;
 * changing the environment in which a job runs (upgrading a library, for example); and
 * changing how jobs get scheduled (not running an expensive job on try, for example).

So we are putting docker images, task definitions, and scheduling information in-tree, where anyone can modify them using the well-established process for making changes to the Firefox source code:
create a patch, test it in try, submit it for review, land it on an integration branch, and watch it "ride the trains" until it is released.

This turns out to be incredibly powerful!
Let's take the example of upgrading a library from the previous section.
The developer looks for some similar bugs, perhaps from the last time this library was upgraded, and learns what changes might be required -- probably just changing a version number in a docker image definition.
Armed with this information, she writes a patch and pushes it to try -- just as she would for a change to the Firefox C++ code.
If the try push succeeds, she pushes the patch to Mozreview, and once the review is complete uses Autoland to land the change.
From there, the sheriffs merge the patch from repo to repo, riding the trains -- so ESR can continue to operate with the old library version until the end of its life, while nightly will use the new version immediately
If something goes wrong, sheriffs back the patch out and its effects are undone.

## How Does It Work?

We have a nice overview of the gecko build process in [the TaskCluster documentation](https://docs.taskcluster.net/tutorial/gecko-tasks).

## Future

At the moment, only about 20% of the total CI workload runs in TaskCluster.
The rest is scheduled by and run in Buildbot, and thus not especially "self-serve".
Soon we will be scheduling all tasks -- even Buildbot tasks -- in-tree, using the Buildbot Bridge to run those tasks within Buildbot.
This will improve the scheduling self-service, providing a nice stepping-stone to actually running all jobs in TaskCluster.

You may have noticed that the top two platforms for Firefox -- Windows and OS X -- are not mentioned here, and don't (yet) support Docker.
We don't have a great self-serve solution for configuring build and test environments on these platforms.
That said, we are working on solutions and experimenting with new technologies as they become available.

We're already seeing a blossoming of creative ideas for the CI system that were simply impractical before.
As more and more of the CI system is defined in-tree, expect to see -- or maybe even implement! -- more cool new features from your CI.
