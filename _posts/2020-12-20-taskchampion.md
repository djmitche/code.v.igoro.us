---
title: Introducing TaskChampion
layout: post
date:   2020-12-20 00:00:00
categories: [taskwarrior]
---

[TaskWarrior](https://taskwarrior.org/) has a bit of a cult following.
It's a command-line task tracking app.
No fancy web UI, not even a desktop UI, just your tasks, simply presented and easily updated.
I've been using it for years now, and even wrote a [Gist about my use of the tool](https://gist.github.com/djmitche/dd7c9f257306e6b8957759c4d5265cc9) to share with my co-workers.

It's not bare-bones, and has some really appealing, nicely-designed features, among them:
 * It's easy to add tags and other information to tasks so that you can pull up just the tasks you need to see.
 * It can synchronize the task list among multiple devices (laptop, desktop, phone..).
 * Tasks have a calculated "urgency" that can help bubble the most important tasks to the top of the list.
 * It supports task dependencies, due dates, and delaying tasks, so you don't have to even think about tasks that you can't start on right now.
 * There are lots of tools to integrate with it, such as [Bugwarrior](https://bugwarrior.readthedocs.io/en/latest/).

The downside is, there are a couple of serious bugs.
Synchronization fails quite often for any but the most trivial uses.
Quoting issues mean that integrations like Bugwarrior can cause errors that require manually editing the DB.
Some of the features like recurring tasks have bugs that cause them to recur too often.
The list goes on.
And, at least [until recently](https://github.com/GothenburgBitFactory/taskwarrior/releases/tag/v2.5.2), it has been unclear when or if new releases would occur, and thus when those bugs might be fixed.


