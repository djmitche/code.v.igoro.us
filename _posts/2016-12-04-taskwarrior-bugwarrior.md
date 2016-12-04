---
layout: post
title:  "Connecting Bugzilla to TaskWarrior"
date:   2016-12-04 11:22:00
categories: [mozilla]
---

I've mentioned before that I use [TaskWarrior](http://taskwarrior.org/) to organize my life.
Mostly for work, but for personal stuff too (buy this, fix that thing around the house, etc.)

At Mozilla, at least in the circles I run in, the central work queue is Bugzilla.
I have bugs assigned to me, suggesting I should be working on them.
And I have reviews or "NEEDINFO" requests that I should respond to.
Ideally, instead of serving two masters, I could just find all of these tasks represented in TaskWarrior.

Fortunately, there is an integration called [BugWarrior](https://bugwarrior.readthedocs.org) that can do just this!
It can be a little tricky to set up, though.  So in hopes of helping the next person, here's my configuration:

    [general]
    targets = bugzilla_mozilla, bugzilla_mozilla_respond
    annotation_links = True
    log.level = WARNING
    legacy_matching = False

    [bugzilla_mozilla]
    service = bugzilla
    bugzilla.base_uri = bugzilla.mozilla.org
    bugzilla.ignore_cc = True
    # assigned
    bugzilla.query_url = https://bugzilla.mozilla.org/query.cgi?list_id=13320987&resolution=---&emailtype1=exact&query_format=advanced&emailassigned_to1=1&email1=dustin%40mozilla.com&product=Taskcluster
    add_tags = bugzilla
    project_template = moz
    description_template = http://bugzil.la/{{bugzillabugid}} {{bugzillasummary}}
    bugzilla.username = USERNAME
    bugzilla.password = PASSWORD

    [bugzilla_mozilla_respond]
    service = bugzilla
    bugzilla.base_uri = bugzilla.mozilla.org
    bugzilla.ignore_cc = True
    # ni?, f?, r?, not assigned
    bugzilla.query_url = https://bugzilla.mozilla.org/query.cgi?j_top=OR&list_id=13320900&emailtype1=notequals&emailassigned_to1=1&o4=equals&email1=dustin%40mozilla.com&v4=dustin%40mozilla.com&o7=equals&v6=review%3F&f8=flagtypes.name&j5=OR&o6=equals&v7=needinfo%3F&f4=requestees.login_name&query_format=advanced&f3=OP&bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&f5=OP&v8=feedback%3F&f6=flagtypes.name&f7=flagtypes.name&o8=equals
    add_tags = bugzilla, respond
    project_template = moz
    description_template = http://bugzil.la/{{bugzillabugid}} {{bugzillasummary}}
    bugzilla.username = USERNAME
    bugzilla.password = PASSWORD

Out of the box, this tries to do some default things, but they are not very fine-grained.
The `bugzilla_query_url` option overrides those default things (along with `bugzilla_ignore_cc`) to just sync the bugs matching the query.

Sadly, this does, indeed, require me to include my Bugzilla password in the configuration file.
API token support [would be nice](https://github.com/ralphbean/bugwarrior/issues/238) but it's not there yet -- and anyway, that token allows everything the password does, so not a great benefit.

The query URLs are easy to build if you follow this one simple trick:
Use the Bugzilla search form to create the query you want.
You will end up with a URL containing `buglist.cgi`.
Change that to `query.cgi` and put the whole URL in BugWarrior's `bugzilla_query_url` parameter.

I have two stanzas so that I can assign the `respond` tag to bugs for wihch I am being asked for review or needinfo.
When I first set this up, I got a lot of errors about duplicate tasks from BugWarrior, because there were bugs matching both stanzas.
Write your queries carefully so that no two stanzas will match the same bug.
In this case, I've excluded bugs assigned to me from the second stanza -- why would I be reviewing my own bug, anyway?

I have a nice little `moz` report that I use in TaskWarrior.
Its output looks like this:

	ID  Pri Urg  Due        Description
	 98 M   7.09 2016-12-04 add a docs page or blog post
	 58 H   18.2            http://bugzil.la/1309716 Create a framework for displaying team dashboards
	 96 H   7.95            http://bugzil.la/1252948 cron.yml for periodic in-tree tasks
	 91 M   6.87            blog about bugwarrior config
	111 M   6.71            guide to microservices, to help folks find the services they need to read th
	 59 M   6.08            update label-matching in taskcluster/taskgraph/transforms/signing.py to use
	 78 M   6.02            http://bugzil.la/1316877 Allow `test-sets` in `test-platforms.yml`
	 92 M   5.97            http://bugzil.la/1302192 Merge android-test and desktop-test into a "test" k
	 94 M   5.96            http://bugzil.la/1302804 Ensure that tasks in a taskgraph do not have duplic
