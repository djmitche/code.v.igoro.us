---
layout: post
title:  "Happy Ada Lovelace Day"
date:   2010-03-25 14:35:00
---


Yesterday, March 24, was Ada Lovelace Day.  I was at [Pumping Station: One](http://pumpingstationone.org/2010/03/lady-ada-lovelace-day-at-psone-tomorrow/),
 and decided to spend an hour or so writing something to honor the first
 computer programmer.  I was feeling singularly uninspired, and googling
 for "Ada Lovelace" didn't turn up anything interesting.  But it did
give me an idea: write a program that googles for you!

I
haven't written much JavaScript lately, but I've heard a lot about the
work Google's done to provide easy JavaScript libraries and APIs.  I
thought it'd be interesting to try out some of these APIs.  It was!  I
hacked up a quick HTML page, using a [Searcher](http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_GSearch) object, to search for Lovelace images.  Here's the code:

The
only downside I've found is that even if you request a "large" result
set, you only get 8 results.  I don't know of a way to get subsequent
results.  So this really only cycles through a few images.  Still, it
only took me an hour, and most of that was remembering how to use the
DOM.

