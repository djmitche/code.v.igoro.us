---
layout: post
title:  "Adapting Users to Our Interfaces"
date:   2016-09-01 11:22:00
categories: [mozilla]
---

The microwave in my kitchen has a timer on it, which I use when making coffee: TIMER-4-0-0-START.
When the time expires, it beeps incessantly at me.
The natural reaction from decades of operating microwaves is to hit CANCEL at this point to get the beeping to start.

However, this doesn't work.
In fact, the designers of the microwave (GE, though probably not here in Schenectady) must have known this, perhaps through user research.
When I hit CANCEL, the LED display scrolls a message: PRESS TIMER.

Stop and think about that for a minute.
The engineers got feedback that users were hitting CANCEL to stop a beeping timer, and their reaction was to waste precious RAM and programmer time to educate the user about which button to use.
Undoubtedly, this was more work than the other option: canceling a beeping timer when the user presses CANCEL.

Lots of software seems to suffer from the same error.
For example, Mercurial often has several ways to achieve the same goal, but only one is "blessed" by the designers.
When I use the wrong command, Mercurial helpfully tells me what I should have typed, presumably hoping that by the repetition of typing this I will eventually learn not to be so stupid.

In this case, I have used `hg add` to add a file which I later refactored out of existence:

    $ hg rm somefile.js
    not removing somefile.js: file has been marked for add (use forget to undo)

The message isn't even clear!
I don't want to "undo" something -- I want to remove a file.
I suppose removing a file is always an "undo", as the file was created at some point, but that's getting a little philosophical.
How about this:

    $ hg rm somefile.js
    somefile.js: removed

I'm sure there are reasons for `hg rm` to not do what I mean.
They likely center around not losing data, as that seems to be the driving force behind a lot of its design (despite Mercurial having slaughtered more hours of my work than Git by a long shot).
I'm sure there's reasons for the CANCEL button to not cancel things, too, based in some similar notion of design purity.

The moral of the story is: if your users are "misusing" your interface, *adapt the interface*, instead of trying to adapt the user.
