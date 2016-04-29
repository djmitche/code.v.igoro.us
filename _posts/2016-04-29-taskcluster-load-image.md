---
layout: post
title:  "Loading TaskCluster Docker Images"
date:   2016-04-29 17:23:00
categories: [mozilla,taskcluster]
---

When TaskCluster builds a push to a Gecko repository, it does so in a docker image defined in that very push.
This is pretty cool for developers concerned with the build or test environment: instead of working with releng to deploy a change, now you can experiment with that change in try, get review, and land it like any other change.
However, if you want to actually download that docker image, `docker pull` doesn't work anymore.

The image reference in the task description looks like this now:

    "image": {
        "path": "public/image.tar",
        "taskId": "UDZUwkJWQZidyoEgVfFUKQ",
        "type": "task-image"
    },

This is referring to an artifact of the task that built the docker image.
If you want to pull that exact image, there's now an easier way:

    ./mach taskcluster-load-image --task-id UDZUwkJWQZidyoEgVfFUKQ

will download that docker image:

    dustin@dustin-moz-devel ~/p/m-c (central) $ ./mach taskcluster-load-image --task-id UDZUwkJWQZidyoEgVfFUKQ
    Task ID: UDZUwkJWQZidyoEgVfFUKQ
    Downloading https://queue.taskcluster.net/v1/task/UDZUwkJWQZidyoEgVfFUKQ/artifacts/public/image.tar
    ######################################################################## 100.0%
    Determining image name
    Image name: mozilla-central:f7b4831774960411275275ebc0d0e598e566e23dfb325e5c35bf3f358e303ac3
    Loading image into docker
    Deleting temporary file
    Loaded image is named mozilla-central:f7b4831774960411275275ebc0d0e598e566e23dfb325e5c35bf3f358e303ac3
    dustin@dustin-moz-devel ~/p/m-c (central) $ docker images
    REPOSITORY          TAG                                                                IMAGE ID            CREATED             VIRTUAL SIZE
    mozilla-central     f7b4831774960411275275ebc0d0e598e566e23dfb325e5c35bf3f358e303ac3   51e524398d5c        4 weeks ago         1.617 GB

But if you just want to pull the image corresponding to the codebase you have checked out, things are even easier: give the image name (the directory under ``testing/docker``), and the tool will look up the latest build of that image in the [TaskCluster index](https://tools.taskcluster.net/index/):

    dustin@dustin-moz-devel ~/p/m-c (central) $ ./mach taskcluster-load-image desktop-build
    Task ID: TjWNTysHRCSfluQjhp2g9Q
    Downloading https://queue.taskcluster.net/v1/task/TjWNTysHRCSfluQjhp2g9Q/artifacts/public/image.tar
    ######################################################################## 100.0%
    Determining image name
    Image name: mozilla-central:f5e1b476d6a861e35fa6a1536dde2a64daa2cc77a4b71ad685a92096a406b073
    Loading image into docker
    Deleting temporary file
    Loaded image is named mozilla-central:f5e1b476d6a861e35fa6a1536dde2a64daa2cc77a4b71ad685a92096a406b073
