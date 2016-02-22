---
layout: post
title:  "TaskCluster Login: Now With LDAP!"
date:   2016-02-22 13:30:00
categories: [mozilla,taskcluster]
---

[TaskCluster](https://tools.taskcluster.net/) has a sophisticated access-control mechanism based on "[scopes](http://docs.taskcluster.net/presentations/scopes/)" that governs every API call.
A push to try requires 42 scopes!

As a guiding principle, and a convenience to users, the TaskCluster team has tried to align users' scopes with their commit privileges.
That is, if you can make some API call via a push to try, you should be able to make that same API call directly.
Typically, users want to copy a task, modify it, and re-run it via [https://tools.taskcluster.net](https://tools.taskcluster.net/).
The [TaskCluster-Login](https://login.taskcluster.net) service supported logins via either Okta (Mozilla, Inc.'s single-signon provider) or Mozillians.
However, Mozillians does not track commit privileges, and Okta is only available to Mozilla employees, so non-employee contributors were left without a means to log in with the full set of scopes they deserved.

Well, no more.
As of last week, the login service supports authentication with an LDAP username and password for those who cannot access Okta.
The practical result is, if you have permission to push to try (SCM level 1 or higher), but no Okta account, you can now access TaskCluster and do anything your try pushes can.

Over the coming month we will be deploying a number of additional improvements to the TaskCluster login experience:

 * Create your own credentials (clientId and accessToken) with limited scopes
   * Temporary credentials for a one-off project
   * Permanent credentials for a command-line tool

 * Better credential management on the tools page
   * See your clientId, what scopes you have, and when the scopes expire
   * Switch between different sets of credentials
   * Grant another site some of your scopes (via an OAuth-like flow)
