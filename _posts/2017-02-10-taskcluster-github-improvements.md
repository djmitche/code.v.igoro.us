---
layout: post
title:  "TaskCluster-Github Improvements"
date:   2017-02-10 11:22:00
categories: [mozilla,taskcluster]
---

Repositories on Github can use TaskCluster to automate build, test, and release
processes.  The service that enables this is called, appropriately enough,
[taskcluster-github](https://docs.taskcluster.net/manual/integrations/github).

This week, Irene Storozhko, Brian Stack, and I gathered in Toronto to land some
big improvements to this service.

First, the service [now supports "release"
events](https://medium.com/@bugzeeeeee/release-events-in-taskcluster-ad593a244e91),
which means it can trigger tasks when a new release is added to github, such as
building and uploading binaries or making release announcements.

Second, we have re-deployed the service as an
[integration](https://developer.github.com/early-access/integrations/) Irene
[has
developed](https://medium.com/@bugzeeeeee/taskcluster-github-bulletin-d827313686b7).
This makes the set-up process much easier -- just go to
https://github.com/integration/taskcluster and click "Install".  No messing
with web hooks, adding users to teams, etc.

The integration gives users a great deal more control over our access to
repositories: it can be installed organization-wide, or only for specific
repositories.  The permissions required are much more restricted than the old
arrangement, too.  On the backend, the integration also gives us much better
access to debugging information that was previously only available to
organization administrators.

Finally, Irene has developed a [quickstart
page](https://tools.taskcluster.net/quickstart/) to guide new users through
setting up a repository to use TaskCluster-Github.  With this tool, we hope to
see many more Mozilla projects building automation in TaskCluster, even if
that's as simple as running tests.
