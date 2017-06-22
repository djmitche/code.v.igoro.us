---
layout: post
title:  "Taskcluster Manual Revamp"
date:   2017-06-22 11:22:00
categories: [mozilla,taskcluster]
---

As the Great Taskcluster Migration draws near the finish line, we are seeing people new to Taskcluster and keen to take advantage of its new features every day.
It's exciting to build something with such expressive power: easy-to-use loaners, automatic toolchain builds, and a simple process for adding new tests, to name just a few.

We have long had a thorough [reference section](https://docs.taskcluster.net/reference), with technical details of the various microservices and workers that comprise Taskcluster, but that information is a bit too deep for a newcomer.
A few years ago, we introduced a [tutorial](https://docs.taskcluster.net/tutorial) to guide the beginning user to the knowledge they need for their use-case, but the tutorial only goes so far.

Daniele Procida gave [a great talk at PyCon 2017](http://pyvideo.org/pycon-us-2017/how-documentation-works-and-how-to-make-it-work-for-your-project.html) about structuring documentation, which came down to this diagram:

     Tutorials   | How-To Guides 
    -------------|---------------
     Discussions | Reference     

This shows four types of documentation.
The top is practical, while the bottom is more theoretical.
The left side is useful for learning, while the right side is useful when trying to solve a problem.
So the missing components are "discussion" and "how-to guides".
Daniele's "discussions" means prose-style expositions of a system, organized to increase the reader's understanding of the system as a whole.

Taskcluster has had a manual for quite a while, but it did not really live up to this promise.
Instead, it was a collection of documents that didn't fit anywhere else.

Over the last few months, we have refashioned the [manual](https://docs.taskcluster.net/manual) to fit this form.
It now starts out with a gentle but thorough description of tasks (the core concept of Taskcluster), then explains how tasks are executed before delving into the design of the system.
At the end, it includes a bunch of use-cases with advice on how to solve them, filling the "how-to guides" requirement.

If you've been looking to learn more about Taskcluster, check it out!
