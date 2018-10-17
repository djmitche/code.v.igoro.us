---
layout: post
title:  "Eight Years at Mozilla"
date:   2018-10-18 12:00:00
---

I started at Mozilla on October 18, 2010, eight years ago today.
Four years ago, I wrote a [retrospective blog post](http://code.v.igoro.us/posts/2014/10/four-years-at-mozilla.html) for my first four years.
Now is a good time to look back over the second half of my time here.

But I also predicted that Mozilla would return to its roots as a community organization focused on the health of the Internet, rather than a small mobile software vendor.
This was wishful thinking in 2014, but happily has come to pass.
Mozilla has a broad portfolio of active projects and products supporting the future of the web, many of them broadly inclusive of contributions outside the company.

## Four Years!

So, what have the last four years looked like?

 * I've moved to the Taskcluster team and risen from "the new guy" to a team tech lead
 * I've learned to write JavaScript -- a lot of it!
   I still love Python, but day-to-day work is in JS.
 * I worked on a detailed analysis of Taskcluster scopes in an effort to remove use of the dreaded "star scope".
   This led to some careful work with Jonas Jensen to add features such as [parameterized roles](http://code.v.igoro.us/posts/2017/12/parameterized-roles.html) that make scopes both more expressive and more specific.
 * I [revamped](http://code.v.igoro.us/posts/2017/06/taskcluster-manual.html) the Taskcluster documentation, partly as an outcome of the process of understanding it myself.
 * I [built](http://code.v.igoro.us/posts/2016/02/taskcluster-login-ldap.html) and [rebuilt](http://code.v.igoro.us/posts/2016/03/taskcluster-login-creds-mgmt.html) the Taskcluster login system as Persona (the federated identity service) was deprecated and later as Okta was replaced with Auth0.
   In the process, I was part of a chorus advocating for an authentication system spanning employees and non-employees, as core to the Mozilla mission.
 * I worked on the "Buildbot Migration" with the Taskcluster team, Release Engineering, and lots of other Mozillians.
   This project moved the entirety of Firefox CI -- build, test, and release -- from Buildbot to Taskcluster.
   The last bit of Buildbot was finally turned off [just last month](https://atlee.ca/blog/posts/so-long-buildbot.html).
 * An important part of that migration was [in-tree](http://code.v.igoro.us/posts/2016/08/whats-so-special-about-in-tree.html) taskgraph generation.
   This solves the complex problem of defining all of the work required to build, test, and release Firefox.
   And it does so in a manner that is approachable and maintainable.
   This has already enabled a bunch of new work including a fantastic new try specification, in-tree compiler upgrades, addition of project-specific tasks, and more.
 * Along with Brian Stack and Hassan Ali, I developed a way for user interfaces to trigger "actions" on an existing CI process (cancelling, retriggering, and so on).

In terms of career growth, I mentioned in 2014 that [I was a "staff" (P4) level](https://gist.github.com/djmitche/2a61ef749da776d080bd53182ab2f126) engineer.
I am still at that level, but hoping to achieve "senior staff" (P5) soon.
Mozilla's "Job Family Architecture" defines these levels in terms that tie directly to Mozilla's mission.
The elevator pitch for P5 is, "provide direction to multiple teams, building experts around you."

From a technical perspective, it involves projects that have company-wide impact, along with consideration of risk and strategy around those projects.
Taskcluster is certainly such a project, as are some of the other activities mentioned above.
I hope I can be effective in transitioning Taskcluster to a "product" that can be [packaged](http://code.v.igoro.us/posts/2018/05/shipped-and-hosted-software.html) and used outside of Firefox CI and even outside of Mozilla.
That is no small feat, and will involve focused effort from a broad group of people both inside and outside the Taskcluster team.

In terms of people and influence, P5 engineers are expected to work across teams and help others learn new skills.
That involves a lot of mentorship and collaboration, as well as consideration of others' strengths in planning technical strategy.
I've gotten myself involved in some hiring projects at Mozilla, as well as deepening my involvement in Outreachy.
But I still struggle with mentorship of peers -- Mozilla does not have anything in place to support this, leaving potential mentors to have awkward and potentially insulting conversations: "Do you want some mentorship on this?"

## Predictions

I made some predictions in 2014, and most missed the mark.
In particular, I predicted that systems would be secure by design and that spam, fraud, and cyberwarfare would be tamed.
A look at the news from any week this year shows that to be utterly false.

Instead, the raw ugliness of humanity is on the march:
liars and bullies really do come out ahead;
truth and fact-based reasoning are out of vogue;
most people do not take important things seriously and are easily influenced; and
there are powerful forces in society bent on hurting other people to serve their own selfish ends.
It's a massively unstable world and predictions even at the three- or six-month range are, I think, foolish.

I hope that, over the next four years, Mozilla can have a bigger impact on the future of the web -- and through it on the world.
And I hope that I can increase my impact on the company and on the software-development industry in general.
