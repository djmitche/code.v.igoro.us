---
layout: post
title:  "PyCon US 2018 Wrapup"
date:   2018-05-17 21:14:00
categories: [mozilla]
---

I attended PyCon US in Cleveland over the last week. Here's a quick summary of the conference.

Aside from my usual "you should go to PyCon" admonition, I'd like to suggest
writing a summary like this every time you visit a conference. It's a nice way
to share what you found valuable with others, and also to evaluate the utility
of attending the conference.

I barely write a lick of Python anymore, so I mostly attend PyCon for the people and for the ideas.
ome themes are common to PyCon: data science, machine learning, education, and core language.
Of course, there's always a smattering of other topics, too.

During the poster session, I saw a poster on the [Python Developers Survey 2017](https://www.jetbrains.com/research/python-developers-survey-2017/) from JetBrains.
One statistic that surprised me: 50% of respondents use Python primarily for data analysis.

# Talks

There were a lot of good talks this year, although few that will [be remembered forever](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript).
Here are a few highlights from the talks I attended.
Sadly, [PyVideo](http://pyvideo.org/) does not have the videos up yet, but I'm sure they will soon be available at http://pyvideo.org/events/pycon-us-2018.html.

I'm trying to get more comfortable with the ideas around machine learning, without actually doing any of the work myself.

* [Deconstructing the US Patent Database](https://us.pycon.org/2018/schedule/presentation/113/) - some technical issues cut the talk short, but Van went into lots of interesting details about analysis of the US patent database, both the language and the attached images.
  It seems the project was leading toward a way to find prior art quickly.
  On particularly neat tool was a concept unique identifier - CUI - that replaces technical terms with an arbitrary identifier.
  It comes from the medical field, and allows disambiguating similar terms and combining multiple terms for the same concept.

* [Birding with Python and Machine Learning](https://us.pycon.org/2018/schedule/presentation/151/) was a much lighter approach to ML.
  Kirk set up a webcam in his backyard and used ML to identify the presence of birds in-frame, and then to try to identify the type of bird.

* [Listen, Attend, and Walk](https://us.pycon.org/2018/schedule/presentation/132/) was a more research-focused talk about interpreting natural-language navigational instructions.
  Padmaja talked in detail about the configuration of a RNN to parse simple English sentences and use them to navigate a DOOM-like environment.
  While the result wasn't exactly magical, I appreciaed the deep, but math-light explanation of the design of the system.

On the core language, I listened to [Dataclasses: The code generator to end all code generators](https://us.pycon.org/2018/schedule/presentation/94/) and [Get your resources faster, with importlib.resources](https://us.pycon.org/2018/schedule/presentation/162/).

Maybe quantum computing is the next big thing? I sat in on [Python for the quantum computing age](https://us.pycon.org/2018/schedule/presentation/147/), where Ravi gave a nice overview of what quantum computing *is*.
He also gave some examples of controlling (real, cloud-based) quantum computers using Python.
Quantum computers still have 10-20 gates, so they can't exactly "run Python", but you can build a basic quantum logic circuit with Python and execute it to get the result.

Sometimes the best talks are those that tell a great story.
[Don't Look Back in Anger](https://us.pycon.org/2018/schedule/presentation/125/) was one of those - Lilly told the story of Edward Orange Wildman Whitehouse and the failure of the first trans-Atlantic telegraph cable.
Besides being funny and an interesting piece of history, she compared the experience to modern "go-live" events and helped illustrate the need for care and planning.
[Reinventing the Parser Generator](https://us.pycon.org/2018/schedule/presentation/143/) was also a fun story.
Dave described, using his typical live-coding style, what a parser generator is, how PLY worked back in the 90's, and how SLY uses new Python magic to do similarly expressive, cool things.
Dave is a *fantastic* teacher, from whom I have learned a great deal, and it's worth noting you can [take private classes with him](https://www.dabeaz.com/).
They are well worth your time.

Yi Ling gave a great keynote on web application vulnerabilities, told in the style of a children's book.
I found the content useful - basically, how not to be stupid when building a website - but the presentation was quite engaging.

I found [What Is This Mess](https://us.pycon.org/2018/schedule/presentation/88/) amusing and informative, too.
Justin talked about writing tests for untested code -- a common situation in my day-to-day work.
His advice was good and illustrated with simple but clear examples.
I think I liked the talk more for the "yes, someone understands me!" factor than anything I learned from it!

# "Hallway Track"

The hallway track -- conference lingo for the interesting stuff that happens outside of the talks -- is strong at PyCon.
During the Expo (filled with vendors and swag I don't really want) I made it a point to sit down at diverse-looking tables and chat with people.
I met people from finance, college students, data scientists, googlers, and a whole host of interesting people.
Working for Mozilla is, of course, a nice conversation starter.

Because I'm staying with family here in Cleveland, I did not participate in any of the evening activities.
That's been a bit of a disappointment -- the dinners are always engaging -- but probably best for family harmony.

On Sunday, there are simultaneous job fairs and poster sessions in the expo hall.
I'm not looking for a job (although the Java recruiters remain hopeful), so I perused the posters.
It's a mix of topics, from genomic and ML research to cool new tools through programming education and civic data projects.
A few were particularly interesting to me.

A poster on the [Pulp project](https://pulpproject.org/) attracted my attention since it seems to solve a recurrent problem at Mozilla: mirroring large binary repositories in a consistent fashion.
The system supports docker images as well as JS and Python packages, and can release repositories that are internally consistent: the packages are all known to work with each other.
This may be useful for deploying Taskcluster, and is also useful for the Firefox CI system to ensure that it can reliably reproduce Firefox builds even if the sources for the build tools fail or disappear.

I talked for some time with some people from the Fedora CommOps team.
They work on operational support for building and supporting the Fedora community.
Since we have an ongoing Outreachy project to build a new version of [Bugsahoy](https://www.joshmatthews.net/bugsahoy/), I was interested in how Fedora connects new contributors to their first contribution.
Their tool, [easyfix](http://fedoraproject.org/easyfix/), seems a little overwhelming to me, but can offer some inspiration for our effort.
More interesting, Fedora uses an archived message bus (fedmsg) to track events in the Fedora ecosystem over time.
This allows creation of leaderboards and other interesting, motivational statistics on new contributions.

# Sprints

PyCon's sprints start after the main conference ends.
The idea is to give projects time to gather together while everyone is in the same location.
PyCon supplies space, power, wifi, and occasionally food.
This year, the wifi and power were strong and the food somewhat disappointing.
The spaces were small windowless conference rooms, and somehow I found them stifling - I guess I've gotten used to working at home in a room full of windows.

I spent the day hacking on [Project Mesa](https://github.com/projectmesa/mesa), like I did last year.
I have no real connection to this project, but the people who work on it are interesting and smart, and I can make a useful contribution in a short amount of time.

I had hoped to meet up with other Outreachy folks, but plans fell through, so I only stuch around for the first day of sprints.
I suspect that if I was more engaged with Python software on a day-to-day basis, I would have found more to hack on.
For example, the Pallets project (the new umbrella for lots of Python utilities like Click and Werkzeug) had a big crowd and seemed to be quite productive.
We could also hear the Django room, where a round of applause went up every time a contribution was merged.

# Come To PyCon

Plan to come next year!

PyCon is an easy conference to attend.
It's in Cleveland again next year, right on the waterfront, near the science museum and the rock-and-roll hall of fame, so if you bring family they will have ample activities.
The conference provides [childcare](https://us.pycon.org/2018/childcare/) if your family is of the younger persuasion.
Breakfast and lunch are included, and dinners are optional.
Every talk is live-captioned on a big screen beside the presenter, so if you have difficulty hearing or understanding spoken English PyCon has your back.
Finanical aid is available.
There's really no reason not to attend!

Registration starts in early spring.
