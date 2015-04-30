---
layout: post
title:  "New Tooltool in Production"
date:   2015-04-30 12:00:00
---

A few weeks ago, I [wrote about the new tooltool](http://code.v.igoro.us/posts/2015/04/tooltool-uploads.html).
Now, finally, that new tooltool [is deployed](https://bugzilla.mozilla.org/show_bug.cgi?id=1155238) in production.
Specifically, the relevant [mozharness](https://hg.mozilla.org/build/mozharness/rev/06a2bc3e6b42) and [gecko](https://hg.mozilla.org/integration/fx-team/rev/c982ce92229b) patches are landed.

So, what does this mean for you?

# I Run Mozharness Scripts on My System

You probably have a `.mozilla/credentials.cfg` file containing a base64-encoded version of your LDAP username and password (you are being careful with that file, right?).
You'll need to [get a relengapi token](https://api.pub.build.mozilla.org/tokenauth/) that grants at least `tooltool.download.public`, and `tooltool.download.internal` if you need to use non-public files.
Then just put the resulting token in `.mozilla/credentials.cfg`.
With that in place, tooltool downloads should work as they always have.
If not, verify that you're using a mozharness with the changes from [bug 1155238](https://bugzilla.mozilla.org/show_bug.cgi?id=1155238) included; specifically using `https://api.pub.build.mozilla.org` as the URL.

Note that most files used by most scripts are public, and thus don't technically need any authentication.
However, the scripts are structured to require a credentials file for all downloads, so you'll need to add the file anyway.
Patches accepted!

# I Upload Files to Tooltool

The new tooltool client makes this nice and easy for you.
See [the instructions](https://wiki.mozilla.org/ReleaseEngineering/Applications/Tooltool#How_To_Upload_To_Tooltool) on the wiki.
As with downloading, you'll need a token, but this time one or both of `tooltool.upload.public` and `tooltool.upload.internal`.
You may not have permission to upload - have a look at [your permissions](https://api.pub.build.mozilla.org/auth/) (log in first!) to find out, and contact release engineering if you believe you should have access and do not.

# I Download Files By Hand

If you've build URLs under `https://secure.pub.build.mozilla.org/tooltool` to download files into your local tooltool cache, that will still work, but there's an easier way.
Head over to [the tooltool UI](https://api.pub.build.mozilla.org/tooltool) and search for the file you want.
Then click the download link.

# I Use Explicit Tooltool URLs

Please avoid inserting explicit tooltool URLs into scripts that run in automation, unless you have some mechanism to cache the downloads.
The tooltool client automatically constructs URLs and caches the downloads, so in most cases it is the best choice for such downloads.

That said, you can construct URLs just like you could for the old tooltool.
As a simple example, [https://api.pub.build.mozilla.org/tooltool/sha512/054..9e1](https://api.pub.build.mozilla.org/tooltool/sha512/054fdbe8cb55d1f7592871311c5a9da76710c7a085fd24457644d80aa0ea3c344c57e99aab3a6fb2ec7ed93c15c8f997d5b7b60692c318f9cacad6418bb359e1) is a public copy of the MPL header.

# I Use The `temp-sm-stuff` Files

Tut, tut!
All of those files are now available, publicly, in the new tooltool.
Switch your automation to use the system described above.

# Deprecations

Once things are running smoothly with the new tooltool, we'll be analyzing traffic to all of the old tooltool servers.
Those are:

  * http://tooltool.pvt.build.mozilla.org/pvt/build/
  * http://tooltool.pub.build.mozilla.org/pub/temp-sm-stuff/
  * http://runtime-binaries.pvt.build.mozilla.org/tooltool/
  * https://secure.pub.build.mozilla.org/tooltool/pub/temp-sm-stuff/
  * https://secure.pub.build.mozilla.org/tooltool/pvt/build/

Once traffic from automation has been eliminated, and we see minimal or no use by individual developers, we'll disable each of these servers.

# A Long Process

It's taken a long time to implement this change - building the backend, writing tests for the client, refactoring the client, and finally deploying the client.
It's not been without its bumps, notably the inability to upload to the "old" tooltool, a [rocky rollout on Windows](https://bugzilla.mozilla.org/show_bug.cgi?id=1155257), and [issues running mozharness locally with the new client](https://bugzilla.mozilla.org/show_bug.cgi?id=1159941).

I'm sorry for the trouble all of that caused.
Hopefully the improvements justify the bumps.
