---
title: 'Actions as Hooks'
layout: post
date:   2018-06-15 15:00:00
categories: [mozilla,taskcluster]
---

You may already be familiar with [in-tree actions](https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/actions.html): they allow you to do things like retrigger, backfill, and cancel Firefox-related tasks
They implement any "action" on a push that occurs after the initial `hg push` operation.

This article goes into a bit of detail about how this works, and a major change we're making to that implementation.

## History

Until very recently, actions worked like this:
First, the decision task (the task that runs in response to a push and decides what builds, tests, etc. to run) creates an artifact called `actions.json`.
This artifact contains the list of supported actions and some templates for tasks to implement those actions.
When you click an action button (in Treeherder or the Taskcluster tools, or any UI implementing the actions spec), code running in the browser renders that template and uses it to create a task, using *your* Taskcluster credentials.

I talk a lot about functionality being [in-tree](http://code.v.igoro.us/posts/2016/08/whats-so-special-about-in-tree.html).
Actions are yet another example.
Actions are defined in-tree, using some pretty straightforward Python code.
That means any engineer who wants to change or add an action can do so -- no need to ask permission, no need to rely on another engineer's attention (aside from review, of course).

### There's Always a Catch: Security

Since the beginning, Taskcluster has operated on a fairly simple model: if you can accomplish something by pushing to a repository, then you can accomplish the same directly.
At Mozilla, the core source-code security model is the SCM level: try-like repositories are at level 1, project (twice) repositories at level 2, and release-train repositories (autoland, central, beta, etc.) are at level 3.
Similarly, LDAP users may have permisison to push to level 1, 2, or 3 repositories.
The current configuration of Taskcluster assigns the same scopes to users at a particular level as it does to repositories.

If you have such permission, check out your scopes in the Taskcluster [credentials tool](https://tools.taskcluster.net/credentials) (after signing in).
You'll see a lot of scopes there.

The Release Engineering team has made release promotion an action.
This is not something that every user who can push to level-3 repository -- hundreds of people -- should be able to do!
Since it involves signing releases, this means that every user who can push to a level-3 repository has scopes involved in signing a Firefox release.
It's not quite as bad as it seems: there are lots of additional safeguards in place, not least of which is the "Chain of Trust" that cryptographically verifies the origin of artifacts before signing.

All the same, this is something we (and the Firefox operations security team) would like to fix.

In the new model, users will not have the same scopes as the repositories they can push to.
Instead, they will have scopes to trigger specific actions on task-graphs at specific levels.
Some of those scopes will be available to everyone at that level, while others will be available only to more limited groups.
For example, release promotion would be available to the Release Management team.

## Hooks

This makes actions a kind of privilege escalation: something a particular user can cause to occur, but could not do themselves.
The [Taskcluster-Hooks](https://docs.taskcluster.net/reference/core/taskcluster-hooks/references/api) service provides just this sort of functionality:
a hook creates a task using scopes assiged by a role, without requiring the user calling `triggerHook` to have those scopes.
The user must merely have the appropriate `hooks:trigger-hook:..` scope.

So, we have added a "hook" kind to the action spec.
The difference from the original "task" kind is that `actions.json` specifies a hook to execute, along with well-defined inputs to that hook.
The user invoking the action must have the `hooks:trigger-hook:..` scope for the indicated hook.
We have also included some protection against clickjacking, preventing someone with permission to execute a hook being tricked into executing one maliciously.

### Generic Hooks

There are three things we may wish to vary for an action:
 * who can invoke the action;
 * the scopes with which the action executes; and
 * the allowable inputs to the action.

Most of these are configured within the hooks service (using [automation](https://hg.mozilla.org/build/ci-admin/), of course).
If every action is configured uniquely within the hooks service, then the self-service nature of actions would be lost: any new action would require assistance from someone with permission to modify hooks.

As a compromise, we noted that most actions should be available to everyone who can push to the corresponding repo, have fairly limited scopes, and need not limit their inputs.
We call these "generic" actions, and creating a new such action is self-serve.
All other actions require some kind of external configuration: allocating the scope to trigger the task, assigning additional scopes to the hook, or declaring an input schema for the hook.

### Hook Configuration

The hook definition for an action hook is quite complex: it involves a complex task definition template as well as a large schema for the input to `triggerHook`.
For decision tasks, cron tasks, an "old" actions, this is defined in [`.taskcluster.yml`](https://dxr.mozilla.org/mozilla-central/source/.taskcluster.yml), and we wanted to continue that with hook-based actions.
But this creates a potential issue: if a push changes `.taskcluster.yml`, that push will not automatically update the hooks -- such an update requires elevated privileges and must be done by someone who can sanity-check the operation.
To solve this, [ci-admin](https://hg.mozilla.org/build/ci-admin/) creates tasks hooksed on the `.taskcluster.yml` it finds in any Firefox repository, naming each after a hash of the file's content.
Thus, once a change is introduced, it can "ride the trains", using the same hash in each repository.

## Implementation and Implications

As of this writing, two common actions are operating as hooks: retrigger and backfill.
Both are "generic" actions, so the next step is to start to implement some actions that are not generic.
Ideally, nobody notices anything here: it is merely an implementation change.

Once all actions have been converted to hooks, we will begin removing scopes from users.
This will have a more significant impact: lots of activities such as [manually creating tasks](https://tools.taskcluster.net/task-creator/) (including edit-and-create) will no longer be allowed.
We will try to balance the security issues against user convenience here.
Some common activities may be implemented as actions (such as creating loaners).
Others may be allowed as exceptions (for example, creating test tasks).
But some existing workflows may need to change to accomodate this improvement.

We hope to finish the conversion process in July 2018, with that time largely taken with a slow rollout to accomodate unforseen implications.
When the project is finished, Firefox releases and other sensitive operations will be better-protected, with minimal impact to developers' existing worflows.
