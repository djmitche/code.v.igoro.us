---
layout: post
title:  "TaskCluster-Github: Post Comments and Status Live!"
date:   2017-02-09 18:54:00
categories: [mozilla,taskcluster]
---

The Taskcluster team maintains a Github App named, appropriately enough, "Taskcluster".
When a pull request is created or a change is pushed to a repository, this app can be configured to start tasks automatically.
It's typically used to build or run tests, but the sky is the limit: the full expressive power of Taskcluster is available!

Recently, Alexandre Poirot added support for making updates in the Github UI while a task is running:

 * [createStatus](https://docs.taskcluster.net/reference/integrations/taskcluster-github/references/api#createStatus) allows updates to the commit status, such as to indicate the current phase or to rapidly indicate test failure before the entire task is complete.
 * [createComment](https://docs.taskcluster.net/reference/integrations/taskcluster-github/references/api#createComment) allows the task (or anything with the proper scopes, really) to comment on Github issues and pull requests.

This has been a common request, and the Taskcluster team is excited that Alexandre took the time to implement it.

There's one fly in the ointment: when we set the app up, we did not configure it with permission to comment on issues.
That permission is "read/write issues", and gives the app permission to manipulate all issues in any configured repositories.
It does *not* give the app permission to modify the source code in a repo.

While we can modify the app's permissions, the result is not actually available for use until the relevant Github org administrators "OK" the change.
Thus, this feature may not be available for your organization.
Org admins will get an email when we modify the permission with instructions as to how to accept the new permissions.
