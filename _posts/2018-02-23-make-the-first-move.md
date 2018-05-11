---
title: 'Internship Applications: Make the First Move'
layout: post
date:   2018-02-23 15:00:00
categories: [mozilla,taskcluster]
---

There's an old story about Charles Proteus Steinmetz, a famous GE engineer in the early 20th century.
He was called to one of Henry Ford's factories, where a huge generator was having problems that the local engineers could not solve.
After some investigation and calculation, Steinmetz made a mark on the shell of the generator and told the factory engineers to open that spot and replace the windings there.
He later sent a bill for his services to Henry Ford: $10,000.
Ford demanded an itemized bill -- after all, Steinmetz had only made a single mark on the generator.
The bill came back: "Making chalk mark on generator: $1. Knowing where to make mark: $9,999."

Like electrical engineering, software development is more than just writing code.
Sometimes it can take hours to write a 3-line patch.
The hard part is knowing what patch to write.

It takes time to understand the system you're developing and the systems it interacts with.
Just undersatnding the problem you're trying to solve can take some lengthy pondering.
There are often new programming languages involved, or new libraries or tools.
Once you start writing the code, new complications come up, and you must adjust course.

Experienced software engineers can make this look easy.
They have an intuitive sense of what is important and what can be safely ignored, and for what problems might come up later.
This is probably the most important skill for newcomers to the field to work on.

# Make the First Move

Lately, I've gotten dozens of emails from Google Summer of Code and Outreachy applicants that go like this:

> Dear Sir,
> 
> I am interested in the Outreachy project "...".
> I have a background in JavaScript, HTML, CSS, and Java. 
> Please connect me with a mentor for this project.

I've also seen dozens of bug comments like this:

> I would like to work on this bug. Please guide me in what steps to take.

There is nothing inherently wrong with these messages.
It's always OK to ask for help.

What's missing is evidence that applicant has made *any* effort to get started.
In the first case, the applicant did not even read the full project description, which indicates that the next step is to make a contribution and has links to tools for finding those contributions.
In the second case, it seems that the applicant has not even taken the first steps toward solving the bug.
In most cases, they have not even *read* the bug!

If my first instructions to an applicant are "start by reading the bug" or "taskcluster-lib-app is at https://github.com/taskcluster/taskcluster-lib-app" (something Google will happily tell you in 0.55 seconds), that suggests the applicant's problem-solving skills need some serious work.
While GSoC and Outreachy are meant to be learning experiences, we look for applicants who are able to make the most of the experience by learning and growing on their own.
A participant who asks "what is the next step" at every step, without ever trying to figure out what steps to take, is not going to learn very much.

# Advice

If you are applying to a program like Google Summer of Code or Outreachy, take the time to try to problem-solve before asking for help.
There is nothing wrong with asking for help.
But when you do, show what you have already figured out, and ask a specific question.
For example:

> I would like to work on this bug.
> It seems that this would require modifying the `taskcluster-lib-scopes` library to add a formatter function.
> I can see how this formatter would handle anyOf and allOf, but how should it format a for loop?

This comment shows that the applicant has done some thinking about the problem already, and I can see exactly where they have gotten stuck.
