---
layout: post
title:  "Modern Multiprocessing"
date:   2010-04-12 16:24:00
---


I've
 been thinking a lot lately about the way we accomplish multiprocessing.
  We've seen a significant change in the operation of Moore's law for
CPU speeds: today's CPUs are about the same speed as those of a few
years ago, but they have more cores, and more virtual processors on
those cores.  This is great for heavily-loaded servers, which have
plenty of distinct tasks to place on those cores and VCPUs, but not so
useful for users working with single-threaded applications.

Why
are most applications still single-threaded?  There are lots of good
reasons. Threaded code is harder to write, and not just because it
requires careful analysis and use of synchronization primitives: many
common tasks are difficult to meaningfully parallelize without careful
control over inter-thread communication, and in a portable application
you don't have that kind of control.  Threaded code generally performs
badly on single-CPU systems, which are still common.  Some popular
languages still make threading difficult, at least in a portable
fashion.  And threads are still relatively heavyweight entities in most
operating systems: you don't spawn ten threads to mergesort a 100-item
array.

Some of these problems will go away with a little more time, but some will get worse.  [NUMA](http://en.wikipedia.org/wiki/Non-Uniform_Memory_Access)
 architectures can make sharing data between threads slow.
Hyperthreading and its interaction with processor caches adds yet
another level of unpredictability.

We
know how to build massively parallel systems that run massively parallel
 algorithms.  What is still unknown is how to build portable, simple
software that can run efficiently across a vareity of architectures.
This is a problem of practice, not theory, and there's lots of
interesting work going on in this area.

Of course, there are languages designed explicitly to support communication, such as [Limbo](http://www.vitanuova.com/inferno/papers/limbo.html) or [Erlang](http://www.erlang.org/index.html), [Haskell](http://www.haskell.org/), and [Clojure](http://clojure.org/).
  For the most part, these languages are structured as communicating
sequential processes, which is to say that they represent
multiprocessing as a set of sequential threads that pass information to
one another.  Problems of thread safety are subsumed by the languages,
but mapping the parallelism to available resources is generally left to
the programmer or administrator.

One interesting project is Apple's [Grand Central Dispatch](http://developer.apple.com/mac/articles/cocoa/introblocksgcd.html).
  It defines a simple but highly expressive closure syntax (a block) and
 a mechanism to dynamically schedule execution of such closures
(queues).  Critically, the GCD library takes care of scaling the
parallelism of the queue processing appropriately to the underlying
hardware.  On a single-threaded CPU, this amounts to cooperative
multitasking, but on parallel hardware the operating system can
dynamically allocate virtual CPUs to applications needing more
parallelism.

This topic seems to come up often in my various pursuits, so I will return to it again.

