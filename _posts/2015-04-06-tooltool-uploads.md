---
layout: post
title:  "Tooltool Reimplemented"
date:   2015-04-06 12:00:00
---

# Tooltool

Several years ago, John Ford invented [tooltool](https://wiki.mozilla.org/ReleaseEngineering/Applications/Tooltool).
The idea was simple and elegant: a simple content-addressable store for large binary files used in build and test jobs.
The files were specified in simple JSON "manifests" that could be embedded in-tree, and downloaded with 'tooltool fetch'.
Files could be cached locally, saving bandwidth.
And because the tool verifies the sha512 digests used to address the content, we can be confident that the binary artifacts are delivered as they were uploaded, avoiding the possibility of accidental or malicious corruption.

But the tool had a few issues, too, which have limited its usefulness so far:

 * For a long time the process to upload new files was "find someone in releng".
   That was later fixed, but the upload process was still a clunky rsync-over-ssh process.
 * Initial deployments of tooltool did no caching, causing massive bandwidth usage.
 * Tooltool is tied to expensive NetApp storage and served by web hosts shared with many other services.
 * We have several places in the source that contain urls pointing inside tooltool's server storage; these will become invalid soon.
 * All tooltool files are "private" and not available for public download; even copies of gcc and clang.
   This makes it difficult for users who are not on the VPN to access the files used in builds and tests.
   It also means that tooltool can't be used outside of the releng network without manually priming your cache.
   Among other things, TaskCluster runs outside of the releng network.

The last issue reached a critical point when I began working on porting Android builds to TaskCluster -- tooltool as it stood was basically useless from TaskCluster.
Never one to apply a strip of duct tape when I can make things better instead, I elected to re-implement tooltool in a manner that will hopefully deliver on its original promise.

# The Fix

Amazon S3 seems like the right place to store this data, right?
It's cheaper than NetApp by a long shot, scales all on its own, and has a flexible permissions model.
Even better, it has a feature called "signed URLs" which allows a server to generate a URL which can be used for exactly one purpose.

We also have a nice tool for hosting services with REST interfaces and simple JS UIs: RelengAPI.

So the solution looks something like this.
To download a file, the tooltool client contacts RelengAPI with the desired sha512 digest and, if necessary, credentials.
If the credentials check out, or the file is public, RelengAPI responds with a signed URL for download from S3 in a nearby AWS region.

To upload a file, the client again contacts RelengAPI, this time sending an "upload batch" similar to a version-control commit: a list of files and a commit message.
For any files not already present, RelengAPI responds with a signed URL to upload the file to S3.
The client then uploads the files directly to S3 and calls back to RelengAPI so it can verify the file contents.
In the background, RelengAPi later replicates the file between regions.

You can see the result, if you have the proper permissions, on [RelengAPI](https://api.pub.build.mozilla.org/tooltool/).

# What This Means For You

As of today, all of the files in the "old" tooltool have been uploaded to the "new" tooltool.
The old tooltool mechanism has been shut down.
However, production jobs are not yet looking to the new tooltool for their files.
So, if you need a file uploaded, upload it [using the new mechanism](https://wiki.mozilla.org/ReleaseEngineering/Applications/Tooltool#How_to_upload_files_to_tooltool), and ping me (:dustin) so I can copy it to the old system.
This will avoid any de-synchronization between the two services.
Once the production jobs are all using the new service, we'll deconstruct the old.

And hopefully your world will be a smidgeon happier.
