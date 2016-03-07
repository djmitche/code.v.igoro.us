---
layout: post
title:  "TaskCluster Login: Credential Management"
date:   2016-03-07 20:29:00
categories: [mozilla,taskcluster]
---

In my [last post about TaskCluster Login](/2016/02/taskcluster-login-ldap.html), I described improvements to allow any Mozillian to sign in to TaskCluster with an appropriate access level.

The next step, now in place, is to allow everyone to manage their own credentials, and those of the projects they work on.

## New Features

First, credentials now have names, which helps us humans to tell them apart.
For example, my temporary credential is named `mozilla-ldap/dmitchell@mozilla.com`.
When I sign in, the tools site helpfully shows the name of my credential in the upper-right corner.

Next, everyone can create clients, as long as they begin with your credential name.
For example, Armen can create a client named `mozilla-ldap/armenzg@mozilla.com/mozci-testing` for testing MozCI.
Before today, doing so required pinging someone in #taskcluster and asking nicely.
These clients are automatically disabled when the owner's priveleges change (e.g., by leaving Mozilla or changing groups).

Finally, using some nice [namespaces](http://docs.taskcluster.net/devel/namespaces/), individual teams can now manage everything related to their project.
For example, a person in the `releng` LDAP group automatically has the scope `project:releng:*`, which governs Release Engineering tools such as [Buildbot Bridge](http://hearsum.ca/blog/buildbot-taskcluster-bridge-an-overview.html).
She also controls clientIds beginning with `permanent/releng/`, which are credentials used by Release Engineering services.
A number of other per-project namespaces are included, such as secrets, hooks, and index routes.

## Questions and Future

There's still work to do, as mentioned in the last post.
For example, when credentials expire, the tools page doesn't show any indication until you try to perform some operation and get an error.
I would also like to add support for sharing TaskCluster credentials with other sites -- for example, wouldn't it be great if you logged into RelengAPI via TaskCluster?

As with any change, I'm sure there will be rough edges and issues I haven't anticipated.
Please file any bugs in the *TaskCluster :: Login* component, or ping me (`dustin`) in IRC.

## Cleaning House

With this change, all clients should have nice long names, either associated with a person or with a team.
However, we have a [plethora of clients](https://tools.taskcluster.net/auth/clients/) that do not fit this pattern.
These fall into three categories:

 * "permacreds" created for specific people (e.g., [`DyUwCUOlRJWAOm7OJJWg1g`](https://tools.taskcluster.net/auth/clients/#DyUwCUOlRJWAOm7OJJWg1g), garndt's permacred)
 * service credentials for TaskCluster services (e.g., [`tc-index`](https://tools.taskcluster.net/auth/clients/#tc-index) or [`O6yB_zofTjCAjPSu4iYKoA`](https://tools.taskcluster.net/auth/clients/#O6yB_zofTjCAjPSu4iYKoA))
 * test credentials used for CI tests of the TaskCluster source (e.g., [`tc-hooks-tests`](https://tools.taskcluster.net/auth/clients/#tc-hooks-tests))

Many of these have slugid's for names -- strings that are as ugly as the name suggests!

To clean all of this up, we will be scheduling the permacreds to expire on March 31 and contacting each owner to suggest simply signing in (using temporary credentials) or creating a properly-named client to replace the permacred.
We will be replacing credentials in the last two categories with credentials named `project/taskcluster/*`.
