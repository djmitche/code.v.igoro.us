---
title: 'Design of Task-Graph Generation'
layout: post
date:   2018-05-04 15:00:00
categories: [mozilla,taskcluster]
---

Almost two years ago, [Bug 1258497](https://bugzilla.mozilla.org/show_bug.cgi?id=1258497)
introduced a new system for generating the graph of tasks required for each
push to a Firefox source-code repository. Work continues to modify the expected
tasks and add features, but the core design is stable. Lots of Firefox
developers have encountered this system as they add or modify a job or try to
debug why a particular task is failing. So this is a good time to review the
system design at a high level.

A quick note before beginning: the task-graph generation system is implemented
entirely in the Firefox source tree, and is administered as a sub-module of the
Build Config module. While it is designed to interface with Taskcluster, and
some of the authors are members of the Taskcluster team, it is not a part of
Taskcluster itself.

# Requirements

A *task* is a unit of work in the aptly-named Taskcluster platform. This might be
a Firefox build process, or a run of a chunk of a test suite. More esoteric
tasks include builds of the toolchains and OS environments used by other tasks;
cryptographic signing of Firefox installers; configuring Balrog, the service
behind Firefox's automatic updates; and pushing APKs to the Google Play Store.

A *task-graph* is a collection of tasks linked by their dependencies. For
example, a test task cannot run until the build it is meant to test has
finished, and that build cannot run until the compiler toolchain it requires
has been built.

The task-graph generation system, then, is responsible for generating a
task-graph containing the tasks required to test a try push, a landing on a
production branch, a nightly build, and a full release of Firefox. That task
graph must be minimal (for example, not rebuilding a toolchain if it has
already been built) and specific to the purpose (some tasks only run on
mozilla-central, for example).

Firefox has been using some CI system -- Tinderbox, then Buildbot, and now
Taskcluster -- for decades, so the set of requirements is quite deep and
shrouded in historical mystery.

While the resulting system may seem complex, it is a relatively simple
expression of the intricate requirements it must meet. It is also designed with
approachability in mind: many common tasks can be accomplished without fully
understanding the design.

# System Design

The task-graph generation process itself runs in a task, called the *Decision
Task*. That task is typically created in response to a push to version control,
and is typically the first task to appear in Treeherder, with a "D" symbol.
The decision task begins by checking out the pushed revision, and then runs the
task-graph generation implementation in that push. That means the system can be
tested in try, and can ride the trains just like any other change to Firefox.

## Task-Graph Generation Process

The decision task proceeds in a sequence of steps:

1. Generate a graph containing all possible tasks (the *full task graph*). As of
   this writing, the full task graph contains 10,972 tasks!

1. Filter the graph to select the required tasks for this situation. Each
   project (a.k.a. "branch" or "repo") has different requirements. Try pushes
   are a very flexible kind of filtering, selecting only the tasks indicated by
   the (arcane!) try syntax or the (awesome!) try-select system (more on this
   below). The result is the *target task graph*.

1. "Optimize" the graph, by trimming unnecessary tasks. Some tasks, such as
   tests, can simply be dropped if they are not required. Others, such as
   toolchain builds, must be replaced by an existing task containing the
   required data.  The result is the *optimized task graph*.

1. Create each of the tasks using the Taskcluster API.

The process is [a bit more
detailed](https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/taskgraph.html#graph-generation)
but this level of detail will do for now.

## Kinds and Loaders

We'll now focus on the first step: generating the full task graph. In an effort
to segment the mental effort required, tasks are divided into *kinds*.  There
are some obvious kinds -- build, test, toolchain -- and a lot of less obvious
kinds.  Each kind has a directory in
[`taskcluster/ci`](https://searchfox.org/mozilla-central/source/taskcluster/ci/).

Each kind is responsible for generating a list of tasks and their dependencies.
The tasks for all kinds are combined to make the full task graph.  Each kind
can generate its tasks in a different way; this is the job of the kind's
*loader*.  Each kind has a `kind.yml` which points to a Python function that
acts as its loader.

Most loaders just load task definitions from YAML files in the kind directory.
There are a few more esoteric loaders -- for example, the test loader creates
one copy of each test for each platform, allowing a single definition of, say
`mochitest-chrome` to run on all supported platforms.

## Transforms

A "raw" task is designed for execution by a Taskcluster worker. It has all
sorts of details of the task baked into environment variables, the command to
run, routes, and so on.  We do not want to write expressions to generate that
detail over and over for each task, so we design the inputs in the YAML files
to be much more human-friendly. The system uses *transforms* to bridge the gap:
each task output from the load is passed through a series of transforms, in the
form of Python generator functions, to produce the final, raw task.

To bring some order to the process, there are some specific forms defined, with
schemas and sets of transforms to turn one into the next:

* [Test Description](https://dxr.mozilla.org/mozilla-central/source/taskcluster/taskgraph/transforms/tests.py) -
  how to perform a test, including suite and flavor, hardware features
  required, chunking configuration, and so on.

* [Job Description](https://dxr.mozilla.org/mozilla-central/source/taskcluster/taskgraph/transforms/job/__init__.py) -
  how to perform a job; essentially "run Mozharness with these arguments" or
  "run the Debian package-building process with these inputs"

* [Task Description](https://dxr.mozilla.org/mozilla-central/source/taskcluster/taskgraph/transforms/task.py) -
  how to build a task description; this contains all of the command
  arguments, environment variables, and so on but is not specific to a
  particular worker implementation.

There are several other "descriptions", but these give the general idea.

The final effect is that a relatively concise, readable build description like
this:

```
linux64/debug:
    description: "Linux64 Debug"
    index:
        product: firefox
        job-name: linux64-debug
    treeherder:
        platform: linux64/debug
        symbol: B
    worker-type: aws-provisioner-v1/gecko-{level}-b-linux
    worker:
        max-run-time: 36000
    run:
        using: mozharness
        actions: [get-secrets build check-test update]
        config:
            - builds/releng_base_firefox.py
            - builds/releng_base_linux_64_builds.py
        script: "mozharness/scripts/fx_desktop_build.py"
        secrets: true
        custom-build-variant-cfg: debug
        tooltool-downloads: public
        need-xvfb: true
    toolchains:
        - linux64-clang
        - linux64-gcc
        - linux64-sccache
        - linux64-rust
```

Can turn into a much larger task definition like
[this](https://queue.taskcluster.net/v1/task/OtYCNHmDSreSjvT8PVZWwA).

## Cron

We ship "nightlies" of Firefox twice a day (making the name "nightly" a bit of
a historical artifact). This, too, is controlled in-tree, and is general enough
to support other time-based task-graphs such as Valgrind runs or Searchfox
updates.

The approach is fairly simple: the [hooks
service](https://tools.taskcluster.net/hooks/project-releng/cron-task-mozilla-central)
creates a "cron task" for each project every 15 minutes. This task checks out
the latest revision of the project and runs a mach command that examines
[`.cron.yml`](https://dxr.mozilla.org/mozilla-central/source/.cron.yml) in the
root of the source tree. It then creates a decision task for each matching
entry, with a custom task-graph filter configuration to select only the desired
tasks.

## Actions

For the most part, the task-graph for a push (or cron task) is defined in
advance. But developers and sheriffs often need to modify a task-graph after it
is created, for example to retrigger a task or run a test that was accidentally
omitted from a try push. Taskcluster defines a generic notion of an
["action"](https://docs.taskcluster.net/manual/using/actions/spec) for just
this purpose: acting on an existing task-graph.

Briefly, the decision task publishes a description of the actions that are
available for the tasks in the task-graph. Services like Treeherder and the
Taskcluster task inspector then use that description to connect user-interface
elements to those actions. When an action is executed, the user interface
creates a new task called an *action task* that performs the desired action.

Action tasks are similar to decision and cron tasks: they clone the desired
revision of the source code, then run a mach command to do whatever the user
has requested.

## Multiple Projects

The task-graph generation code rides the trees, with occasional uplifts, just
like the rest of the Firefox codebase. That means that the same code must work
correctly for all branches; we do not have a different implementation for the
mozilla-beta branch, for example.

While it might seem like, to run a new task on mozilla-central, you would just
land a patch adding that task on mozilla-central, it's not that simple: without
adjusting the filtering, that task would eventually be merged to all other
projects and execute everywhere.

This also makes testing tricky: since the task-graph generation is different
for every project, it's possible to land code which works fine in try and
inbound, but fails on mozilla-central. It is easy to test task-graph generation
against specific situations (all inputs to the process are encapsulated in a
`parameters.yml` file easily downloaded from a decision task). The artistry is
in figuring out which situations to test.

## Try Pushes

Pushes to try trigger decision tasks just like any other project, but the
filtering process is a little more complex.

If the push comes with legacy try syntax (`-b do -p win64,linux64 -u
all[linux64-qr,windows10-64-qr] -t all[linux64-qr,windows10-64-qr]` - clear as
mud, right?), we do our best to emulate the behavior of the Buildbot try parser
in filtering out tasks that were not requested. The legacy syntax is deeply
dependent on some Buildbot-specific features, and does not cover new
functionality like optimization, so there are lots of edge cases where it
behaves strangely or does not work at all.

The better alternative is
[try-select](https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/try.html#try-task-config),
where the push contains a `try_task_config.json` listing exactly which tasks to
run, along with desired modifications to those tasks. The command `./mach try
fuzz` creates such a file.  In this case, creating the target task-graph is as
simple as filtering for tasks that match the supplied list.

# Conclusion

This has been a long post! The quote "make everything as simple as possible and
no simpler", commonly attributed to Einstein, holds the reason -- the
task-graph generation system satisfies an incredibly complex set of
requirements. In designing the system, we considered these requirements
holistically and with a deep understanding of how they developed and why they
exist, and then designed a system that was as simple as possible. The remaining
complexity is inherent to the problem it solves.

The task-graph generation is covered in [the Firefox
source-docs](https://firefox-source-docs.mozilla.org/taskcluster/taskcluster/index.html)
and its source is in the
[`/taskcluster`](https://dxr.mozilla.org/mozilla-central/source/taskcluster/)
directory in the Firefox source tree.
