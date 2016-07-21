---
layout: post
title:  "Recovering from TaskWarrior Corruption"
date:   2016-07-20 22:43:00
categories: [mozilla]
---

I use [TaskWarrior](http://taskwarrior.org/) along with [TaskWarrior for Android](https://play.google.com/store/apps/details?id=kvj.taskw&hl=en) to organize my life.
I use [FreeCinc](http://freecinc.com/) to synchronize all of my desktops, VPS, and phone, using a crontask.
Most of the time, it works pretty well.

## FreeCinc Fail

However, yesterday, all of FreeCinc's keys expired.
There's a big red warning on the home page instructing users to download new keys.;
Since my sync's operate on a crontask, I didn't notice this until I discovered tasks I remembered modifying in one place did not appear in another.
By that time, I had modifed tasks everywhere -- a few things to buy on my phone, some work stuff on the laptop, some more work stuff on the VPS, and some personal stuff on the desktop.

So, downloading new keys is easy.
However, TaskWarrior doesn't magically take four different sets of tasks and combine them into a single coherent set of tasks, just by syncing to a server.
No, in fact, since there are no changes to sync, it does nothing.
Just leaves the different sets of tasks in place on different machines.
So basically everything I modified in 24 hours, across four machines, was now unsynchronized.
And I use this to run my life, so it was probably 100 or so changes.

## What Was I Doing Again?

Here's how I fixed this:

I copied `pending.data` and `completed.data` from all four hosts onto a single host.
These files are in a pretty simple one-task-per-line format, with a uuid and modification timestamp embedded in each line.
The rough approach was to take all of the tasks in all of these files, and select most recent instance for each uuid.
There's a little bit of extra complication to handle whether a task is completed or not.
I used the following script to do this calculation:

	import re

	uuid_re = re.compile(r'uuid:"([^"]*)"')
	modified_re = re.compile(r'modified:"([0-9]*)"')
	def read(filename):
		with open(filename) as f:
			for l in f:
				uuid = uuid_re.search(l).group(1)
				try:
					modified = modified_re.search(l).group(1)
				except AttributeError:
					modified = 0
				yield uuid, int(modified), l

	def add_to(uuid, modified, completed, line, coll):
		if uuid in coll:
			ex_modified, ex_completed, _ = coll[uuid]
			if ex_modified >= modified:
				return
			if ex_completed and not completed:
				return
		coll[uuid] = (modified, completed, line)

	by_uuid = {}
	for c, fn in [
		(True, "rama-completed.data"),
		(True, "hopper-completed.data"),
		(True, "dorp-completed.data"),
		(True, "android-completed.data"),
		(False, "rama-pending.data"),
		(False, "hopper-pending.data"),
		(False, "android-pending.data"),
	]:
		for uuid, modified, line in read(fn):
			add_to(uuid, modified, c, line, by_uuid)



	with open("completed-result.data", "w") as f:
		for _, completed, line in by_uuid.itervalues():
			if completed:
				f.write(line)

	with open("pending-result.data", "w") as f:
		for _, completed, line in by_uuid.itervalues():
			if not completed:
				f.write(line)

As it turns out, I might have simplified this a little by looking at the `status` field: `completed` and `deleted` are in `completed.data`, and the rest are in `pending.data`.

Once I was happy with the results (approximately the right number of pending tasks, basically), I copied them into `~/.task` on one machine, and ran some `task` queries to check everything looked good (looking for tasks I recalled adding on various machines).
Satisfied with this, I downloaded yet another set of keys from FreeCinc and installed them on that same machine.
I deleted `~/.task/backlog.data` on that machine (just in case) and ran `task sync init` which appeared to upload all pending tasks.
Great!

Next, I deleted `~/.task/*.data` on all of the other machines, installed the new FreeCinc keys, and ran `task sync`.
On these machines, it happily downloaded the pending tasks.
And we're back in business!

I chose not to just copy `~/.task/*.data` between systems because I run slightly different versions of TaskWarrior on different systems, so the data format might be different.
I might have used `task export` and `task import` with some success, but I didn't think of it in time.
