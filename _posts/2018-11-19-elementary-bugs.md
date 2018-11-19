---
title: Elementary Bugs
layout: post
date:   2018-11-19 15:00:00
categories: [mozilla]
---

Mozilla is a well-known open-source organization, and thus draws a lot of interested contributors.
But Mozilla is huge, and even the more limited scope of Firefox development is a wilderness to a newcomer.
We have developed various tools to address this, one of which was an [Outreachy](https://www.outreachy.org/) project by Fienny Angelina called [Codetribute](http://codetribute.mozilla.org/).

The site aggregates bugs that experienced developers have identified as good for new contributors ("good first bugs", although often they are features or tasks) across Bugzilla and Github.
It's useful both for self-motivated contributors and for those looking for starting point for a deeper engagement with Mozilla (an internship or even a full-time job).

However, it's been tricky to help developers identify good-first-bugs.

# Elementary

I watched a Youtube video, ["Feynman's Lost Lecture"](https://www.youtube.com/watch?v=xdIjYBtnvZU).
It is not the lecture itself (which is lost..) but Sanderson covers the content of the lecture -- "an elementary demonstration of why planets orbit in ellipses".

He quotes Feynman himself [defining "elementary"](https://youtu.be/xdIjYBtnvZU?t=201):

<blockquote>I am going to give what I will call an elementary demonstration.
But elementary does not mean easy to understand.
Elementary means that very little is required to know ahead of time to understand it, except to have an infinite amount of intelligence.</blockquote>

I propose that this definition captures the perfect good-first-bug, too.

# Elementary Bugs

An elementary bug is not an easy bug.
An elementary bug is one that requires very little knowledge of the software ahead of time, except to have the skills to figure things out.

A newcomer does not have the breadth of knowledge that an experienced developer does.
For example, members of the Taskcluster team understand how all of the microservices and workers fit together, how they are deployed, and how Firefox CI utilizes the functionality.
A task that requires understanding all of these things would take a long time, even for a highly skilled newcomer to the project.
But a task limited to, say, a single microservice or library provides a much more manageable scope.

[Bug 1455130, "Add pagination to auth.listRoles"](https://bugzilla.mozilla.org/show_bug.cgi?id=1455130), is a good example.
Solving this bug requires that the contributor understand the API method definitions in the Auth service, and how Taskcluster handles pagination.
It does *not* involve understanding how Taskcluster, as a whole, functions.
So: a little bit of knowledge (of JS, of Git, of HTTP APIs), and the skills to jump into a codebase, find similar implementations, adopt a coding style, and so on.

Having completed a bug like this, a budding contributor can use their newfound understanding as a home base to start exploring related topics.
Having understood that the Auth services is concerned with Clients and Roles, what are those?
How do they relate to permissions to do things, and what sort of things?
What scopes are required to create a task?
What can a task do?
Before long, the intrepid contributor is a Taskcluster pro..

Other forms of elementary bugs might include:
 * Refactoring an existing, well-tested function (so, only need to understand what the function does and how to do it better)
 * Adding unit tests for well-factored functions (but not integration tests, which by their nature require too much knowledge of how things fit together)
 * Implementing a new component from a well-defined specification (such as a new React component)

By contrast, some things do not make good first bugs:
 * Repetitive tasks such as renaming or fixing lint (but note that these can be good for practicing version-control processes!)
 * Open-ended debugging, which often involves a lot of intuition (born of experience) and digging through layers a newcomer will not be familiar with
 * Anything requiring design, as a newcomer lacks the perspective to evaluate designs' suitability to the situation

I have found the term "elementary" to be a helpful yardstick in evaluating whether to tag something as a good-first-bug.
Hopefully it can help others as well!
