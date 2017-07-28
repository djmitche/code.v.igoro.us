---
title: Taskgraph Optimization
layout: post
date:   2017-07-27 19:00:00
---

For every push to a Gecko repository, and for periodic things like nightlies,
we [generate a
task-graph](http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/index.html)
containing all of the tasks to run in response. This is all controlled in-tree,
making it easy for any developer to add new tasks when necessary.

The full task-graph is currently just over 8000 tasks, and growing.  Running
8000 tasks for every push would be slow and wasteful, so we have two mechanisms
to limit the tasks we run. The first is "target tasks", which selects the
desired tasks based on try syntax or the tree to which the push took place. The
second is the topic of this post: optimization.

# Why Optimization?

Before diving into the details, let's address why optimization is important.

First and foremost, in many cases it gets important results back to developers
sooner, increasing development velocity. Not displaying feedback unrelated to a
push also helps to focus attention on the important results.

Optimization also helps to ease real resource issues Mozilla faces.  Tasks such
as Talos or OS X tests must run on our own hardware, and we have a finite (but
large - about 500 just for OS X!) quantity of that hardware. When the quantity
of work to do exceeds the capacity of that hardware pool, tasks begin to queue,
delaying important feedback to developers. Buying more hardware is always an
option, but the fixed costs and long lead times mean that effort spent
optimizing the work done on the existing assets has a big return.

Most tasks take place in the cloud (AWS), which provides a more elastic
environment that is able to burst when load is high. We run well over 10,000
spot instances simultaneously every business day, producing terabytes of data.
Even at pennies per hour and gigabyte, that quickly adds up to "real money".
Reducing that cost, or limiting its growth, is an important goal in its own
right.

Optimization has risks, too: over-optimization can skip tasks with important
information. That might mean that a try push looks fine but has failures when
it lands, or that push containing an error appears green but causes a failure
on a subsequent push. In any case, time-consuming bug hunts and backouts ensue.

The try server causes a lot of consternation - it's difficult to figure out
what syntax to use to run all of the tasks that might be relevant to a push,
resulting in either over-estimation (and thus wasted capacity) or
under-estimation (risking missed bugs and backouts). Ideally, machines could
figure this out: a push to try with no syntax would run just the necessary
jobs, no more and no less.

# Optimization Today

Back to the task-graph generation process. During the optimization step, each
task is examined for reasons that it might not be run. For some tasks, such as
[toolchain](https://hg.mozilla.org/mozilla-central/file/36f95aeb4c77/taskcluster/taskgraph/transforms/job/toolchain.py#l45)
or [docker
image](https://hg.mozilla.org/mozilla-central/file/36f95aeb4c77/taskcluster/taskgraph/transforms/docker_image.py#l37)
builds, it is possible to find and substitute an existing task that used the
same inputs.
[SETA](https://elvis314.wordpress.com/2015/02/06/seta-search-for-extraneous-test-automation/)
also applies at this stage.

Finally, some jobs are annotated with
"[when.files-changed](https://hg.mozilla.org/mozilla-central/file/36f95aeb4c77/taskcluster/taskgraph/transforms/job/__init__.py#l64)",
a list of filename patterns. When the set of files changed in a push does not
match this list, the job is optimized away.

This works well for some tasks.  For example, [the eslint
task](https://hg.mozilla.org/mozilla-central/file/36f95aeb4c77/taskcluster/ci/source-test/mozlint.yml#l1)
lists all files that might contain Javascript, along with configuration and
source for the linting process. But it doesn't scale to more complex or common
jobs. For example, consider what files should be included for a mochitest run
on OS X? In general, this approach is verbose and couples the task descriptions
tightly to the source code.

# Optimization Tomorrow

Fine-tuning when we run eslint is only 1/8000'th of the problem. We need an
approach to optimization that can take some "big bites" out of task graphs,
such as omitting entire platforms or test suites. We have done a little of this
for servo, e10s, and a few other projects, but using ad-hoc approaches.

While pursuing large impact, we need to ensure we do not over-optimize, so the
approach must fail open: if in doubt, a task should run.  Once wasteful runs
are observed, it should be fairly simple to define the circumstance and
represent that in code. This approach is the opposite of "when.files-changed",
which over-optimizes unless the author has named every file that might affect
the task.

## Tagging

The proposed approach is to tag each source file with named task groups that it
"affects". In this case, "affects" is taken strictly. For example, a change to
a chrome file is best tested by the `browser-chome` suite, but could
potentially affect other tests or even builds if it contains a syntax error.
However, a [push containing only changes under
`layout/reftests`](https://hg.mozilla.org/mozilla-central/rev/32a63be) cannot
possibly affect anything but reftests. Similarly, [changes limited to
`mobile/android`](https://hg.mozilla.org/mozilla-central/rev/0f58f328) cannot
possibly affect any platform but Android.

The tagging is done using familiar clauses in `moz.build` files:

    with Files('mobile/android/**'):
        AFFECTS_TASKS += ['android']

(note that this syntax is illustrative; the details are not yet decided)

To "fail open", files which do not have any tags are treated as having all
tags.  Given these annotations, for a given push, it is straightforward to
calculate the set of affected tags.

## Task Configuration

Task configuration can contain an [optimization
element](https://hg.mozilla.org/mozilla-central/file/36f95aeb4c77/taskcluster/taskgraph/transforms/task.py#l138)
specifying a set of tags containing this task:

    label: android-test-android-4.3-arm7-api-15/debug-reftest-1
    optimizations:
        - [skip-unless-affects, [android, reftests]]

Meaning, skip unless the changes affect either `android` or `reftests`.  In
most cases, this value would be calculated by the
[transforms](http://gecko.readthedocs.io/en/latest/taskcluster/taskcluster/transforms.html)
rather than included directly in the YAML source files.

## Practical Examples

Directories such as `mobile/android` or `browser/` that are only used on
certain platforms are an easy target. Changes limited to these directories can
omit entire platforms.

Test-only changes can also be aggressively optimized.  While each test file
technically affects only one task, we can achieve a good balance of
effectiveness and detailed configuration by tagging by test suite
(browser-chrome, wpt, mochitest, etc.)

Servo synchronizes its changes into the `servo/` directory in the Gecko source
tree, and changes to that directory only realistically affect the `linux64` and
`linux64-servo` platforms. Tagging `servo/**` with `servo`, and adding `servo`
to `skip-unless-affects` for tasks on those two platforms would be enough to
achieve this result, with the advantage that tasks for other platforms can be
re-added easily using the "add jobs" or "backfill" actions in Treeherder.
