---
layout: post
title:  "Ad-hoc Tasks in TaskCluster"
date:   2015-07-02 12:00:00
categories: ['taskcluster']
---

You may have heard of [TaskCluster](https://docs.taskcluster.net), and you may have heard that it's the bees' knees.
All of that is true, but I won't reiterate here.

# Ad-Hoc Tasks

We have a number of things we need to build from time to time that aren't part of the normal CI process.
Typically, these have been built on someone's laptop and uploaded as-is, perhaps with some copy-paste into a wiki page or the like.
This can lead to some unhappy surprises when the dependencies change due to differences in the build environment, or when the re-creation instructions aren't quite accurate.

Well, TaskCluster can help!

First, you can run arbitrary things in TaskCluster very easily.
Just head over to the [Task Creator](https://tools.taskcluster.net/task-creator/) and click "Create Task".
The default echoes "Hello World", but it's easy to see how to proceed from there.
So if a task is simple enough to be embedded in a shell one-liner, you're already done.
Just paste the task description into an in-tree comment or the relevant bug, and the next person to replicate your work can just re-run that task.

But most tasks are a little more complicated.
Consider:

 * Building gcc or clang for use building Gecko
 * [Building cctools for Mac-on-Linux cross compilation](https://bugzilla.mozilla.org/show_bug.cgi?id=1176229)
 * Building RPMs or DEBs for deployment to other infrastructure (e.g,. with Puppet)
 * [Packaging Java JRE and JDK for use from tooltool](https://bugzilla.mozilla.org/show_bug.cgi?id=1161075)
 * Downloading and re-packaging Android NDKs and SDKs
 * Building the signmar binary for use on signing servers

None of these are especially difficult, but none are as simple as a one-liner.

# Example

For these cases, we have a means to run arbitrary in-tree scripts.
It starts by adding a script under `testing/taskcluster/scripts/misc` to do what you need done.
For example, I've written [this script](https://bitbucket.org/djmitche/mozilla-central/src/8a7b7cc73ee8/testing/taskcluster/scripts/misc/repackage-jdk.sh) to repackage the Ubuntu build of OpenJDK for use in ToolTool.
Note that this script drops its results in `~/artifacts`.

Then, push the commit containing that script somewhere public, like your user repo, and [submit a docker-worker task](https://tools.taskcluster.net/task-inspector/#SUGE4XlqSFmzoKPq1uyNlg/).
In this case, the payload looks like this:

    {
      "image": "quay.io/djmitche/desktop-build:0.0.19",
      "command": [
        "/bin/bash",
        "-c",
        "cd /home/worker/ && ./bin/checkout-sources.sh && ./workspace/build/src/testing/taskcluster/scripts/misc/repackage-jdk.sh"
      ],
      "env": {
        "GECKO_HEAD_REPOSITORY": "https://bitbucket.org/djmitche/mozilla-central",
        "GECKO_HEAD_REV": "be2867e357f7",
        "VERSION": "7u79-2.5.5-0ubuntu0.14.04.2"
      },
      "artifacts": {
        "public": {
          "type": "directory",
          "path": "/home/worker/artifacts",
          "expires": "2015-07-02T14:58:41.058Z"
        }
      },
      "maxRunTime": 600
    }

Running this is as simple as pasting it into the Task Creator.

The image given here is the current docker image used for desktop builds.
The command is also similar to what's used for desktop builds -- it checks out the tree, then runs the script.
I provide arguments as environment variables -- the gecko repository and version (pointing to the user repo) and the OpenJDK version to package.

The "artifacts" portion is how we get the files out of the task.
It specifies the in-container directory containing the files we want to make available.
Anything in that directory on completion of the task will be available for download in the task inspector (or via automated means, but for ad-hoc tasks like this the UI is easiest).

The task description is fairly generic, but it's still useful to include the payload in the bug where you run the script for future archaeologists to find.

# Summary

So there you have it.
TaskCluster is useful not only for performing massive numbers of continuous-integration tasks, but for running one-off tasks in a reproducible, inspectible, secure fashion.

# More!

Ted has noted that `checkout-sources.sh` is pretty heavy-weight: it checks out gecko, mozharness, and build/tools!
For many scripts, we can probably do much better with a simpler [single script bootstrap](https://bugzilla.mozilla.org/show_bug.cgi?id=1179893) script.
