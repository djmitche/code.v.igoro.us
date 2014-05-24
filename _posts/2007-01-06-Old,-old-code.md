---
layout: post
title:  "Old, old code"
date:   2007-01-06 15:40:00
---


Once upon a time, I was a member of the [Syzygy
Cult](http://www.syzygycult.com/), an active game-development group for the
680x0 macs.  Among the many games we wrote was **Mantra**, an adventure game
with a top-down view similar to Legend of Zelda.  Recently, the source code has
re-surfaced (one of the other members found it in his parents' basement over
the holidays). Judging by the dates in the source files, I was 16 at the time
this was written, which means I had been programming for about 8 years.  At a
general level, I'm blown away by the level of organization we had:

*   Meeting minutes show we discusesd, agreed upon, and wrote down apolicy for organizing header files: one per source file, with a singleheader that included all of them as well as common system includes.

*   Several source files are annotated with e.g., "Reviewed DJM 6/23/94" -- we were doing _code review!_
*   The graphics routines were written in hand-tuned assembly.

*   We used double-buffering to achieve smooth scrolling.

*   We "hired" a graphic designer (as in, went out and found a guywe didn't know who would work for free) and gave him really explicit,detailed requests

My main contributions to the project were the graphics code (which also handled
pixel-wise intercept detection) and the various in-game dialogs, like the items
screen and the stores.

In a way, I feel like I've fallen off the trajectory I was on at that time.  If
I was writing code like this at 16, after eight years of programming, where am
I now, after twenty years?

