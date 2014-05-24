---
layout: post
title:  "Testing Legacy Code"
date:   2010-02-17 13:26:00
---


I just read Roy Osherove's [The Art of Unit Testing with Examples in .NET](http://www.amazon.com/Art-Unit-Testing-Examples-Net/dp/1933988274),
 on the advice of a slashdot review.  I was not terribly impressed with
the book, but reading it did help me to solidify my thinking about
testing and test-driven development, and put words to concepts I had
come to on my own.

Rather late in the book, Osherove describes three properties of good tests.

*   _Trustworthiness_ - Do developers believe that passing testsmean things are working? Do developers believe that failing testsindicate a real bug?
*   _Maintainability_ - Do developers think that tests are easy to add and maintain, or are they likely to avoid writing tests when rushed?
*   _Readability_ - Do developers often consult the unit tests to see how the system under test is supposed to work?

What
most struck me was that these properties were related to developers'
perceptions of the tests, not the tests themselves.  Tests are as much a
 social artifact of a project as a technical tool.

## Buildbot's Tests

Around
 the time I was reading this, one of the more prolific Buildbot
contributors commented, "I try not to change the tests - they scare me."
  Buildbot's tests were badly isolated, slow, and failed intermittently.
  As maintainer, I had grown accustomed to saying "oh, that test fails
sometimes, don't worry about it" - a trustworithiness failure.  Because
of the terrible isolation, changing just about anything in Buildbot
would cause dozens of tests to fail, requiring repetitive editing to fix
 - not maintainable.  And the tests consisted of long sequences of
operations and assertions, written in the Twisted style, which is
already not readable.  As a result, even I don't know what most of the
tests are actually testing.  This was a bad situation for any
application, but particularly embarassing for a popular testing tool!

So I **blew the tests away**.  Well, not really - I moved them to <tt>buildbot/broken_test/</tt> in hopes they can be useful in writing new tests, and so that the braver souls among us can still run them.  Now our [metabuildbot](http://buildbot.net/metabuildbot/tgrid) is green, and I can legitimately ask for unit tests for new code.

There
 are costs associated with this move, too. A lot of people have worked
very hard to write tests that have now been categorically labeled
"broken," to whom all I can say is "I'm sorry".  With far fewer tests
and thus far worse coverage, it's also difficult to have confidence that
 Buildbot really works.  The short-term workaround is to make a few [beta releases](http://comments.gmane.org/gmane.comp.python.buildbot.devel/5703) and rely on real-world testing to suss out any problem.

So
this is only the first step.  We - I - still need to write real tests
for the vast majority of the Buildbot code.  That's particularly
complicated because Buildbot's units are badly isolated, and interfaces
are ill-defined.  I will need to do a good bit of refactoring to bring
it into compliance.

