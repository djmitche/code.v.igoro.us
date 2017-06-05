---
layout: post
title:  "PyCon US 2017 Wrapup"
date:   2017-06-04 22:54:00
categories: [mozilla]
---

I attended PyCon US in Portland two weeks ago. Here's a quick summary of the conference.

The tl;dr is: if you do anything in Python, or are interested in data science,
science software, or programming education for children, come to PyCon. Come
for the conference and hallway track, and plan to stay for the sprints.

# Talks

I don't do a lot of Python these days, so I didn't have any particular topic to focus on.
Instead, I tried to pick talks where I'd learn something, without a lot of regard for *what* I would learn.
Here's a selection of the more interesting talks I found:

 * *[Next Level Testing](http://pyvideo.org/pycon-us-2017/next-level-testing.html)*
   (James Saryerwinnie) -- Discussion of property testing, coverage-driven fuzzing, stress testing, and mutation testing.
   Property testing sounds particularly cool, as it can take a very general property (`func` should not raise any exception but ValueError) and explore inputs until it finds one that violates the property.
   This could be useful in programming against specs or comparing pre- and post-refactor behavior in a big refactor.

 * *[A Gentle Introduction To Deep Learning with Tensorflow](http://pyvideo.org/pycon-us-2017/a-gentle-introduction-to-deep-learning-with-tensorflow.html)*
   (Michelle Fullwood) -- Last year I attended a talk about deep learning "for non-rocket scientists" that was so densely packed with math that I gave up.
   This talk was much better, and I now feel like I have an understanding of how deep learning works, how it's related to regression and modelling, and issues around overfitting.

 * *[Do It For Science](http://pyvideo.org/pycon-us-2017/keynote-do-it-for-science.html)*
   (Katy Huff) -- This was a great keynote emphasizing the importance of supporting science and exhorting all of us to get involved.
   She brought up a number of concrete suggestions, including Software Carpentry, Data Carpentry, The Hacker Within, and JOSS.
 
 * *[What Nobody Tells You About Documentation](http://pyvideo.org/pycon-us-2017/how-documentation-works-and-how-to-make-it-work-for-your-project.html)*
   (Daniele Procida) -- This was a high-level, but meaningful talk about documentation.
   It divided documentation into four types: tutorial (to learn), how-to (to solve problems), reference (to get information), and discussion (to gain understanding).
   He made some links between these -- two are practical, two are theoretical, two are good for studying, and two are good when using the product.
   I think too many products just lump all of their documentation together, making it hard or impossible to find what you need when you need it.
   Reading API docs is not a great way to learn how a library works, but neither is reading a chapter about the software a good way to remember what the name of that method you need is.

 * Finally, *[Hacking Cars With Python](http://pyvideo.org/pycon-us-2017/hacking-cars-with-python.html)* (Eric Evenchick)
   and *[Hacking Classic Nintendo Games with Python](http://pyvideo.org/pycon-us-2017/hacking-classic-nintendo-games-with-python.html)* (Sam Agnew)
   were cool dives into the bits-and-bytes world of digital devices around us.  Sam's actually involved hacking an emulator,
   and Eric's did not involve any actual cars (in fact, I don't remember much Python), but both shared the excitement of
   being able to modify a system's behavior by peeking and poking bytes here and there.

# "Hallway Track"

The hallway track -- conference lingo for the interesting stuff that happens outside of the talks -- is strong at PyCon.
That starts with chatting up others at lunch or at the numerous tables in the hallways ("So, how do you use Python?" is a good starter).
After a few years (I've been at PyCon since 2011!), you start to see the same people and have something to catch up on.

PyCon hosts conference dinners each year, some with Python-related trivia.
These are a nice mix: a fun social time with lots of conversational topics, but still enough of a "conference event" to feel safe and relaxed.
The Python trivia was hard!
For example, can you name -- off the top of your head -- the keyword with the most characters?

I attended a few "open spaces".
These are organized at the event, by pinning index cards to a timeslot on a big pin-board in the lobby - sort of like an unconference.
These can be social events, organized meetings, or just people interested in a topic gathering to chat.
One evening I attended "PyMicrobreweries" which was a fancy name for a handful of strangers heading to Rogue together.

I also dropped in on a Mozilla Science Lab chat led by [Danielle Robinson](https://twitter.com/daniellecrobins).
I didn't know much about the Science Lab, but I learned quite a bit from Danielle and the others present and got connected to some of the lab's activities, including the [Mozilla Global Sprint](https://mozilla.github.io/global-sprint/).

# Sprints

PyCon's sprints start after the main conference ends.
The idea is to give projects time to gather together while everyone is in the same location.
Some projects take advantage of the time for core developers to meet and make momentous decisions.
Some projects use the time to get some work done - writing code, tending to issues, etc.
And some projects use the audience to attract new contributors.
The latter make sprints a great time for newcomers to the language to get some experience with real Python software, and to learn from some of the best.

The sprints are *extremely* informal.
There's no schedule at all -- the allotted days are completely open.
The conference provides a few meeting rooms, tables, along with power and Internet.
Some years, there's lunch, some years everyone at the table pitches in for a Subway order.
This year, a box lunch was provided every day.

I keep feeling like I should care more about the Internet of Things, so my initial plan was to hack on [Mycroft](https://mycroft.ai/).
I had some trouble installing it before the conference, so that seemed like a good place to start: get that fixed and then do something to help the next person avoid the issue.
This turned out to take a while, though, and I found a few more issues along the way.
The team turned out to be all dudes, and I wasn't getting a great sense of open-source-ness, so I wandered away mid-morning.

I spent the rest of the day hacking on [Project Mesa](https://github.com/projectmesa/mesa), an agent-based modeling tool.
This ticked a few boxes for me: Python-3 only, science-related, and not one of the "major" frameworks like Pandas or NumPy.
I worked on some issues around random-number generator seeding (so that interesting or buggy runs can be re-created), and refactoring the examples to follow the new best practices for models.
I learned a bit about agent-based modeling, Jupyter notebooks, and how a library like this gets used to do science.
And I got to meet a bunch of interesting people, which is really the best reward!

It's worth noting that last week, Mozilla Science held its [Global Sprint](https://science.mozilla.org/programs/events/global-sprint-2017), a distributed version of the same idea.
I got a chance to work on another science-related tool there, [phageParser](https://github.com/phageParser/phageParser).
