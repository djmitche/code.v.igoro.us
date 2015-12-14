---
layout: post
title:  "Taskcluster Security Exercise"
date:   2015-12-14 12:00:00
categories: [mozilla,taskcluster]
---

During [Mozlando](https://wiki.mozilla.org/Coincidental_work_weeks/2015_Orlando) last week, I organized a TaskCluster "security game".
The goals of this exercise were:

 * Learn to think like an attacker
 * Develop ideas for monitoring for, preventing, and reacting to attacks
 * Share awareness of the security considerations around TaskCluster

The format was fairly simple: participants were given with a number of "tasks" and a set of credentials with a relatively low access level (SCM level 1, or permission to push to try).
I added some ground rules to prevent mayhem and to keep the difficulty level reasonable.
Several members of the Infosec team participated, along with most of the TaskCluster team and a few Release Engineering folks.

## Rules

Most of us have "administrator" credentials which would allow us to accomplish any of these tasks easily.
Those credentials are off-limits for the duration of the exercise: no heroku access, no github pushes, no use of your AWS credentials. 
Only public, read-only access to `taskcluster/*` Docker Hub repos is allowed, although you are free to push to personal repos, public or private.

What you do have is the client-id `red-team` with an access key that will be provided on the day of the exercise.
It has scope `assume:moz-tree:level:1`, which is try-level access.
If you manage to reveal other credentials during the course of the exercise, you are of course free to use them.

You are permitted to push to try (gaia or gecko) under your own LDAP account.
Pushes to sheriffed trees are not allowed.

Do not perform any actions intended to or reasonably likely to cause a denial of service for other TaskCluster users.
If something breaks accidentally, we will end the exercise and set about fixing it.

We can consider removing some of these restrictions next time, to model rogue-insider, credential-disclosure, or DoS scenarios.

## Tasks

 * Make an API request with clientId `red-team-target`.

 * Display the relengapi token used by the relengapi proxy in a task log.

 * Submit a task that adds an artifact to a different task.

 * Claim, "execute" by logging "OWNED!", and resolve a task with a provisionerId/workerType corresponding to existing infrastructure (docker-worker, generic-worker, funsize, signing, buildbot bridge, etc.)

 * From a task, create a process that sends traffic to <IP address> and continues to do so _after_ the task has ended.

 * From a task, cause another host within the AWS VPC to execute arbitrary code.

 * Harvest a secret value from a private docker image.

 * Via a task, start a shell server on the docker-worker host (outside of the container) and connect to it.

 * Create a "malicious" binary (not necessarily Firefox) and sign it with a real Mozilla signing key.

## Results

I won't go into detail here, but we were able to accomplish a few of these tasks in the 3 hours or so we spent trying!
Most began by extracting secrets from a private docker image -- one of the oldest and most-discouraged ways of using secrets within TaskCluster.

## Next Time

I'd like to run an exercise like this at every coincidental work-week (so, every 6 months).
We wrote down some ideas for next time.

First, we need to provide better training in advance for people not already familiar with TaskCluster -- Infosec in particular, as they bring a great deal of security and penetration-testing experience to the table.
Even for an expert, three hours is not a lot of time to craft and carry out a complicated attack.
Next time, we could spread the exercise over the entire week, with the ground rules and targets announced on Monday, some shorter hacking sessions organized during the week, and a summation scheduled for Friday.
This would allow ample time for study of the TaskCluster implementation, and for long-running attacks (e.g., trying to exploit a race condition) to execute.

We practice security-in-depth, so some of the vunlerabilities we found could not be further exploited due to an additional layer of security.
Next time, we may hypothesize that one of those layers is already broken.
For example, we may hypothesize that there is a bug in Docker allowing read access to the host's filesystem, and emulate this by mounting the host's `/` at `/host` in docker images for a particular workerType.
What attacks might this enable, and how could we protect against them?

Finally, some members of the Infosec team are interested in running this kind of exercise much more frequently, for other services.
Imagine spending a day breaking into your new web service with the pros -- it might be easier than you think!
