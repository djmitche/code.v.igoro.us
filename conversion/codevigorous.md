### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">USENIX LISA</span>](http://code.v.igoro.us/archives/1-USENIX-LISA.html)<div class="lastUpdated">December 6, 2006 10:17 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

So what better time to inagurate this blog than now, during the [keynote](http://www.usenix.org/events/lisa06/tech/#keynote) to the [LISA (Large Installation Systems Administration)](http://www.usenix.org/events/lisa06/index.html)
 conference.  It's an interesting general talk about one of the many 
pressing non-technical issues in this community: DRM and restrictive 
licensing.  

He's 
boiled it down nicely: in the traditional crypto challenge, Alice 
talking to Bob, with Carol trying to eavesdrop, Carol has the ciphertext
 and the cipher, but not the key -- that's the feature that 
differentiates Carol from Bob, allowing Bob, but not Carol, to decrypt 
it.  But under DRM and other legal challenges Carol and Bob are the same
 person.  Companies are sending cyphertext to Carol/Bob, with the 
restriction that they can use it in one capacity (as Bob, the consumer) 
but not in another (as Carol, the same consumer who wants to watch the 
DVD on her computer).  Obviously, the only technical way to make this 
work is to control the cipher (the algorithm).  It's easy to build a 
cipher to do what they want.  It's technically impossible to prevent 
others from building ciphers that don't.  So they turn to the law.

This 
all reminds me of the "good old days" of the Apple II and crazy 
technical copy-protection schemes -- schemes which faded in popularity, 
and seem to have come back in the last decade.  Doctrow's answer was, to
 put it simply, DMCA. DMCA gave these companies the legal muscle they 
needed.

This 
keynote highlights what I'd like to talk about on this site -- I'm not 
much interested in posting code samples, or kvetching about this 
language or that language.  I'd rather talk about these much more 
important issues.
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">"Teaching Problem Solving: You Can and You Should" (Elizabeth Zwicky)</span>](http://code.v.igoro.us/archives/2-Teaching-Problem-Solving-You-Can-and-You-Should-Elizabeth-Zwicky.html)<div class="lastUpdated">December 6, 2006 11:06 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Mrs.
 Zwicky gave a really excellent talk that balanced real research in 
education, in problem solving, and in systems administration.  She 
teaches systems administration to Navy recruits for a defense 
contractor, in a tutoring setting.  The talk addressed the common belief
 that problem solving skills are essentially innate and can't be taught.
  She discussed the problem-solving process in general, using lots of 
examples (well, "war stories") from systems admin.  Finally, she talked 
about some of the techniques and skills needed to teach problem solving 
(or anything, really).

These
 techniques included scaffolding -- building the learners' conceptual 
understanding by presenting the right tasks, offering the right support,
 and convincing the learner to talk about the concepts, not just "what 
do I type".  Also included was "spotting", which I assume comes from 
sports -- the idea here is to make sure that the learner doesn't suffer 
any horrible consequences from making mistakes. This topic was 
interesting to me, as someone who bridges education, systems 
administration, and development.  I think it's important for 
well-trained, intelligent people to think about and participate in 
education -- systems administrators included (for the record, I'm happy 
with the NSF's requirement that scientists do some sort of "community 
service" as a part of their work for a grant).

I 
found it relevant to me in two ways.  First, the person who replaced me 
at my previous job is a very green admin.  He's been doing basic IT 
legwork for a few years -- repairing computers, user support, etc.  Now 
he's in charge of a heterogenous Linux/Windows shop with a bunch of web 
services, funky applications, and so on.  Since he's in a production 
environment, questions are always "how do I do XYZ?" rather than "how 
does SSL work."  That makes it hard to concentrate on teaching the 
problem-solving that underlies all of this.

I 
have also tried to teach varoius IT-related things to a bunch of 
students (programming, administration, etc.).  For most, the motivation 
was missing, and I never figured out how to get around that.  For one, 
though, I found that spotting was an effective way to motivate her to 
actually try to solve a problem, rather than just requesting and 
following steps.  I asked her to add a printer to a Windows network, but
 said I wouldn't answer any questions, but would fix anything that broke
 while she was working on it.  It took a few iterations of the 
assurances before she started, and it took her a while to work through 
the process, but she now reflects on this as the best learning 
experience of our time working together.

During
 the Q&amp;A session for this talk, I was somewhat disappointed that all
 of the questions focused on Problem Solving / System Administration -- 
horror stories, "what kind of problem solving is this", etc. -- nobody 
was interested in the teaching of these skills.
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Map of IPv4</span>](http://code.v.igoro.us/archives/3-Map-of-IPv4.html)<div class="lastUpdated">December 11, 2006 4:53 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

[This](http://xkcd.com/c195.html)
 is from a web comic, but it's a genius way to lay out the IP space.  I 
particularly like the way you can see the outlines of the old classful 
divisions, and get a good feel for what portion has been allocated.  I'm
 also amused that companies (like Google over on the left) are just 
specks. [![](codevigorous_files/map_of_the_internet.jpg)](http://xkcd.com/c195.html)
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">This should go away!</span>](http://code.v.igoro.us/archives/4-This-should-go-away%21.html)<div class="lastUpdated">January 6, 2007 11:25 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

One
 of the problems with coding in a high-level language is that sometimes 
the insulation from low-level details like memory management is not 
complete.  In this post, I present a method for debugging memory leaks 
in Python.

## Garbage Collection

Python
 has two kinds of memory management: reference counting and a 
mark-and-sweep garbage collector for cycle elimination.  The reference 
counting takes care of immediately finalizing objects when the last 
reference to them goes away, such as when a variable goes out of scope, 
or a key is deleted from a mapping.  This takes care of the vast 
majority of objects, but the programmer has to be careful not to create 
cycles.  For example, consider this tree implementation:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">class Node:
    def __init__(self, parent=None):
        self.children = []
        self.parent = parent
        if parent: self.parent.children.append(self)

def make_tree():
    root = Node()
    kid1 = Node(root)
    kid2 = Node(root)
    return root
</pre>

Now <tt>root</tt>'s <tt>children</tt> references both <tt>kid1</tt> and <tt>kid2</tt>, but each of those nodes reference <tt>root</tt> via their <tt>parent</tt>
 attribute.  This forms a reference cycle (actually two), and simple 
reference counting will not finalize it.  For some time now, Python has 
had mark-and-sweep garbage collection to periodically seek and destroy 
these cycles.  Some time after the last reference to a cycle goes away, 
the garbage collection algorithm runs, identifies the cycle as garbage, 
and finalizes the objects in the cycle.

## Leaks

Even with full garbage collection, it's still easy to "leak" memory in Python:

*   If large objects are involved in a cycle, they may "hold" theirmemory a lot longer than you'd like, leading to a 2-3x increase inmemory consumption, depending on usage patterns.

*   References can get "stuck" in unexpected places, such as <tt>sys.exc_info</tt>, <tt>threading.Thread</tt> instances, or function closures.

*   If an object in a cycle has a finalizer (<tt>__del__</tt>), the garbage-collection algorithm cannot finalize it, and the entire cycle will persist.

## Leak-Hunting

In the process of chasing what turned out to be several leaks in a large, long-running daemon, I developed a tool I'm calling _shouldGoAway_.  The idea is that the application being debugged calls <tt>shouldGoAway(obj)</tt> when it expects <tt>obj</tt> to go away soon.  The tool makes a weak reference to the object and waits one second.  If the object still exists, it uses the <tt>gc</tt> module to construct a reference graph for the object, and dumps that graph to disk in a format readable by [GraphViz](http://www.graphviz.org/).  Here's how it might be used:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">def compute():
    data_structure = get_data()
    process_data(data_structure)
    shouldGoAway(data_structure, "data_structure")
</pre>

The tool itself is [shouldGoAway.py](http://code.v.igoro.us/files/shouldGoAway.py).

### Improvements

*   This module creates a separate <tt>Timer</tt> for every call whichcan lead to a lot of resource consumption if lots of objects should begoing away.  It would probably be sensible to switch to a single threadthat processes objects sequentially.

*   It would be nice to be able to adjust the delay before an object is checked.

*   I think I've struck a nice balance of brevity and useful information in the graph, but there's room for improvement.

*   Many objects (C types, tuples, lists, etc.) are not weak referencable.  It might be nice to work around this.</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Old, old code</span>](http://code.v.igoro.us/archives/5-Old,-old-code.html)<div class="lastUpdated">January 6, 2007 3:40 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Once upon a time, I was a member of the [Syzygy Cult](http://www.syzygycult.com/), an active game-development group for the 680x0 macs.  Among the many games we wrote was **Mantra**,
 an adventure game with a top-down view similar to Legend of Zelda.  
Recently, the source code has re-surfaced (one of the other members 
found it in his parents' basement over the holidays). Judging by the 
dates in the source files, I was 16 at the time this was written, which 
means I had been programming for about 8 years.  At a general level, I'm
 blown away by the level of organization we had:

*   Meeting minutes show we discusesd, agreed upon, and wrote down apolicy for organizing header files: one per source file, with a singleheader that included all of them as well as common system includes.

*   Several source files are annotated with e.g., "Reviewed DJM 6/23/94" -- we were doing _code review!_
*   The graphics routines were written in hand-tuned assembly.

*   We used double-buffering to achieve smooth scrolling.

*   We "hired" a graphic designer (as in, went out and found a guywe didn't know who would work for free) and gave him really explicit,detailed requests

My 
main contributions to the project were the graphics code (which also 
handled pixel-wise intercept detection) and the various in-game dialogs,
 like the items screen and the stores.

In
 a way, I feel like I've fallen off the trajectory I was on at that 
time.  If I was writing code like this at 16, after eight years of 
programming, where am I now, after twenty years?
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Are we really smarter?</span>](http://code.v.igoro.us/archives/6-Are-we-really-smarter.html)<div class="lastUpdated">April 8, 2007 11:10 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

I love reading old computer science texts.  I own the first three volumes of <u>The Art Of Computer Programming</u>,
 and while I can't claim to have read them all cover-to-cover, I often 
flip through them fairly randomly, and usually find some clever 
algorithmic trick or optimization that piques my interest.

Somehow I hadn't heard about [HAKMEM](http://www.inwap.com/pdp10/hbaker/hakmem/hakmem.html) before.  It's an entirely _new_ trove of puzzles to think about! 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Improving svnmerge</span>](http://code.v.igoro.us/archives/7-Improving-svnmerge.html)<div class="lastUpdated">April 23, 2007 7:44 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

There's been a lot of writing about svnmerge: Ken Kinder [wrote a nice introductory article](http://kenkinder.com/svnmerge/) on the topic, and now there's a [wiki](http://www.orcaware.com/svn/wiki/Svnmerge.py) and even a [mailing list](http://www.orcaware.com/mailman/listinfo/svnmerge).  Maybe someday soon it will depart the [contrib/ purgatory](http://svn.collab.net/repos/svn/trunk/contrib/client-side/svnmerge/)!

One
 unusual use of svnmerge is to "branch" a public subversion repository 
into your local repository, to allow local development while still 
tracking the public trunk.  This is related to vendor branches, but is 
more suited to the case where you'll be submitting changes back to the 
project, and is particularly useful if you have commit permission on the
 public repository.  For me, I was merging from the Python repository (<tt>http://svn.python.org/projects/python/trunk/</tt>) to my own private repository (let's call it <tt> http://svn.v.igoro.us/python/trunk</tt>).

Svnmerge
 has a few weaknesses, but one that surprised me was this: while 
svnmerge can manage changes between different repositories, it _can't_ do so when the repository-relative path is the same in each branch.  In this case, the repository-relative path for both is <tt>/python/trunk</tt>, so svnmerge complains:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">svnmerge: cannot init integration source '/python/trunk'
It must differ from the repository-relative path of the current directory.
</pre>

# Getting Under The Hood

To understand why this limitation exists, you need to look at how 
svnmerge works its magic.  For each managed branch, svnmerge keeps a 
list of the revisions in the source branch that have been merged.  By 
default, this list is stored in the property <tt xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">svnmerge-integrated</tt>, looking like <tt xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">/python/trunk:1-54918,54920-54926</tt>.  When merging new changes (<tt xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">svnmerge merge</tt>),
 this property gets updated to reflect the newly merged revisions.  The 
problem, in this case, is that the identifier for the branch does not 
include any information for the repository: does this property list 
revisions in my repository, or in the Python repository?

# The Fix

The 
solution I found to this problem was to qualify the properties with an 
identifier for the repository.  For most repositories, the obvious 
choice is to use a full URL, e.g., <tt>http://svn.python.org/projects/python/trunk:1-54918,54920-54926</tt>.  For repositories which might be accesed via different URLs by different people, the UUID might be a better idea, e.g., <tt>uuid://6015fed2-1504-0410-9fe1-9d1591cc4771/python/trunk:1-54918,54920-54926</tt>.
  To be general, I introduced the notion of a "location identifier" to 
specify the location of a branch.  Currently, there are three location 
identifier formats: 

*   **path**: the "old way" with a simple repository-relative path

*   **url**: a fully qualified URL for the branch

*   **uuid**: a UUID-based identifier

When initializing a new branch, you can specify one of these formats with the <tt>--location-type</tt> flag:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">$ svnmerge init --location-type uuid http://svn.python.org/projects/python/trunk
property 'svnmerge-integrated' set on '.'
$ svn pg svnmerge-integrated .
uuid://6015fed2-1504-0410-9fe1-9d1591cc4771/python/trunk:1-54928
</pre>

# The Future

Subversion
 1.5 promises to support merge tracking natively.  From what little I've
 seen, it does this using a similar technique -- keeping lists of 
revisions in properties.  However, the developers are not recommending 
that folks all convert to 1.5 immediately -- it looks like it will be a 
significant change that needs some serious testing first.  Even if it 
were stable, most Linux distros are so slow to upgrade that it's 
reasonable to assume we'll all be using 1.3 for a good while.

This patch is in the submission process on the mailing list, but an updated version of svnmerge.py is available [on this site](http://code.v.igoro.us/files/svnmerge.py), if you'd like to take it for a spin.  Any feedback would be appreciated!
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Programming Challenge: Sudoku Generator</span>](http://code.v.igoro.us/archives/8-Programming-Challenge-Sudoku-Generator.html)<div class="lastUpdated">April 24, 2007 12:02 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Write a program to generate sudoku puzzles with a unique solution.

In Postscript.  

In such a way that if I print 5 copies of your program, I get five distinct sudoku puzzles.

## Clarifications

*   The puzzles should, at most, specify 25 of the 81 spaces.

*   Programs that simply take an existing puzzle and apply transformations will be frowned upon mightly.

*   If it crashes my printer, it doesn't qualify.</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Open-Source Support?</span>](http://code.v.igoro.us/archives/9-Open-Source-Support.html)<div class="lastUpdated">June 16, 2007 3:01 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

I saw an [interesting post on the Subversion development list](http://svn.haxx.se/tsvn/archive-2007-06/0114.shtml) a while ago.  In part:

> This note is to inform you that the Shell Group will be migrating from 
> Windows 2000 to Microsoft's new operating system known as Windows Vista 
> with effect from Q1 2008, and to seek your assistance and support in 
> minimising disruption to users and applications during and after the 
> migration.

The 
note goes on to request some fairly specific information about the 
upgrade path for TortiseSVN, the Windows Subversion client.  They are 
the sorts of questions that all IT shops would love to ask all of their 
vendors, with the expectation of a full and well-researched answer.  

As
 an admin at a small K-12 school, questions of this sort were met with 
blank stares from vendors.  At best, we could get a demo unit, but any 
sort of analysis of the potential fit of a product (besides the 
"analysis" the salesmen would do) was simply out of the question for an 
account of our size.  On the other hand, I could usually count on honest
 assessments from open-source software mailing lists, even if they 
didn't represent full-scale implementation analyses.

The
 Shell Group request turns the situation around.  Shell Group is a very 
large client and is probably accustomed to contacting peers like Dell, 
Aramark, or HBN-AMRO with requests like this.  Yet here they are making 
these requests of a gaggle of developers, _none_ of whom want to be
 "the main liaison for ALL matters pertaining to Vista compatibility."  
There were no on-list responses, so I can't say what became of the 
request.

There's
 clearly a business need here, but it's not the typical "sell support 
for open source software" niche.  Rather, Shell Group wants a business 
entity with which they can have a more contractual relationship: one 
that can get the software certified by Microsoft, make projections as to
 deliverable dates, and so on.  An entity that can answer support calls 
but does not have significant control of the development community is 
simply not capable of these things, but neither is a development 
community without a legally representative organization.

I'm
 interested to see if this kind of request occurs more often, and what 
effect it has on the landscape of adoption of OSS in big business. 

### Fact-Checking

Some basic googling for other messages like this turned up nothing.  
It's quite possible that this is a hoax.  If so, I'm sorry for promoting
 it, but I think the points it brought up are interesting nonetheless.</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Chicago Coffeeshops</span>](http://code.v.igoro.us/archives/10-Chicago-Coffeeshops.html)<div class="lastUpdated">September 5, 2007 12:04 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Since I telecommute, I spend a lot of time in the house.  Sometimes I just need a change of scenery.  Here are the places I go:

<center xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">

<small>[View Larger Map](http://maps.google.com/maps/ms?ie=UTF8&amp;hl=en&amp;msa=0&amp;msid=113563694508286633526.00000111c2bd77999eb9b&amp;om=1&amp;ll=41.934211,-87.647196&amp;spn=0.284934,0.11842&amp;source=embed)</small></center> </div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Open-source contributors</span>](http://code.v.igoro.us/archives/11-Open-source-contributors.html)<div class="lastUpdated">September 6, 2007 12:58 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

There
 have been a few interesting sites popping up lately to do some 
large-scale analysis of open source applications and the developers 
behind them.  [ohloh](http://www.ohloh.net/) is one such 
site.  Ohloh analyzes the source to extract license and language 
information, and also looks at the relative contributions of various 
authors, based on commits.

The [Amanda report](http://www.ohloh.net/projects/5128?p=Amanda) shows some warnings:

*   Small development team

*   Short source control history

The first is something I'd like to change -- if you're looking for an open source project, have I got a deal for you!

The 
second is actually an artifact of the switch to Subversion -- a much 
longer history is available in SourceForge's CVS repository, but when 
the project switch to subversion, it was imported in a single revision, 
rather than using cvs2svn.

EDIT: fix typo in the title 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Perl vs. Python</span>](http://code.v.igoro.us/archives/12-Perl-vs.-Python.html)<div class="lastUpdated">October 19, 2007 4:05 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Oops.  I inadvertently started a small skirmish in the ongoing language wars.  It began when I [suggested](http://code.v.igoro.us/%3Ca%20href=) rewriting the bulk of [Amanda](http://www.amanda.org/) in a scripting language.

The denizens of this list are mostly seasoned UNIX admins and open 
source programmers with an sysadmin background.  To my understanding, 
this is also the "core constituency" of Perl's popularity -- it's a 
language that lets admins Get Stuff Done.  Parts of Amanda are already 
written in Perl, so I thought Perl was a shoo-in for Amanda's new 
scripting language.

Well, the discussion isn't over yet, but I was very surprised to see that Python, my [BFFL](http://www.urbandictionary.com/define.php?term=bffl)
 among scripting languages, was strongly suggested by a number of 
participants, while only one person offered a solid vote for Perl.

I wonder: have I been out of touch, or are tides starting to shift?  
It's interesting that allegiances would shift for languages which have 
been around for so long (Python [was first released in 1991](http://en.wikipedia.org/wiki/Python_%28programming_language%29), Perl-1.0 [arrived in 1987](http://perldoc.perl.org/perlhist.html)). 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Programming Contests and Puzzles</span>](http://code.v.igoro.us/archives/13-Programming-Contests-and-Puzzles.html)<div class="lastUpdated">December 24, 2007 11:59 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

In August 1992, inCider/A+ magazine ran a programming contest, the rules
 for which were "[U]se the IIGS assembly language source code supplied 
by the FTA to complete their Bouncin' Ferno game."  The game was a 
marble-madness clone, written entirely in assembly by a bunch of French 
hackers.  The code played some fairly devious tricks, as assembly often 
does, and was sparsely commented -- and in French, at that.  Anyway, I 
spent something like a year rewriting the game from scratch, again in 
assembly, and adding a number of new features.  A year later, I won the 
contest (admittedly, probably as the only entrant) and rode a wave of 
fame and fortune through a few random apple user's groups in central 
Maine.

Since then, I've had a fascination with programming contests and related puzzles, even leading me to post a challenge [here in April](http://code.v.igoro.us/archives/8-Programming-Challenge-Sudoku-Generator.html) (which I still haven't solved).

Even though I'm not interested in a new jowerful, intelligent, important people (including the wonderful Donna 
Brazile).

What
 has me upset is that I've now heard two women explain that they don't 
have the "mathematical genius" to work out the proper representation for
 these states; no men have made such a declaration.  First of all, 
that's bull: anyone can work out what 33% of 128 is.  The difficult part
 is in the politics, and everyone on this committee is an expert on 
politics.

More
 importantly, though: why is it OK for these women to brag about their 
mathematical ignorance?  What message does this send to PoliSci students
 struggling through calculus?  One of the women to mention this was 
Alice Travis Germond, who was a VP of NARAL -- hardly an advocate of 
keeping women barefoot, pregnant, and in the kitchen.  What is she 
thinking?

[UPDATE] The other woman to brag about her innumeracy was Tina Flournoy -- Gore's finance director!  Finance! 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">roll back a git-svn mirror</span>](http://code.v.igoro.us/archives/20-roll-back-a-git-svn-mirror.html)<div class="lastUpdated">December 2, 2008 11:15 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Several [Amanda](http://amanda.org/)
 developers use git internally, but the Amanda source code is in 
Subversion at SourceForge.  Git-svn manages bidirectional mirroring for 
us, and works flawlessly.

Recently,
 however, we introduced a problem through user error: due to a typo in 
our git-authors file, a bunch of revisions were mirrored with incorrect 
author information.  This was more than a cosmetic problem because it 
caused the SHA1 hashes to differ between developers who fixed the typo 
at different times (because the author information is included in the 
data that feeds the hash algorithm).  This would leave us with divergent
 commits forever.

The 
challenge, then, is to make git-svn think that it never fetched that 
revision.  HEAD was at r1413, but r1391 had the bad author.  We branched
 for release right after the bum commit, so there are two branches to 
deal with.  Here's what I did:

First, roll back the remote branches (e945b67d78c239b42cb882e5c28e24354d0c05f0 is r1390)

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">$ git update-ref -m "roll back git-svn" ext/trunk e945b67d78c239b42cb882e5c28e24354d0c05f0
$ git update-ref -m "roll back git-svn" -d ext/amanda-261 cad126843a7649ca3e05088dd46ee41d7f17e7e2
</pre>

Next, edit both maxRev values in git-svn's metadata (<tt>.git/svn/.metadata</tt>):

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">[svn-remote "ext"]
    reposRoot = https://amanda.svn.sourceforge.net/svnroot/amanda
    uuid = a8d146d6-cc15-0410-8900-af154a0219e0
    branches-maxRev = 1413
    tags-maxRev = 1413
</pre>

Finally, delete the ._ref_log

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">$ rm .git/svn/ext/trunk/.rev_map*
$ rm .git/svn/ext/amanda-261/.rev_map*
</pre>

Then just re-run the fetch:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">$ git svn fetch ext
</pre></div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">git prompt addition</span>](http://code.v.igoro.us/archives/22-git-prompt-addition.html)<div class="lastUpdated">February 1, 2009 1:25 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Now
 that I'm using git all the time, it's helpful to have bash show me what
 branch I'm on, and whether the working directory is dirty.  I found a [gist by Henrik Nyh](http://henrik.nyh.se/2008/12/git-dirty-prompt)
 that does just this.  I souped it up a little bit to be more efficient 
and handle a few extra situations.  Here's the result:
[EDIT: I have updated this gist since this post was made; the current 
version is based on git-completion.sh in the git distrut this file is not present in the distribution.  I removed it from 
the Makefile.  Presumably I'll be on my own to configure serial I/O?

I'm 
starting to get the impression that using the IDE is the smart way to go
 here!  The next error is from the linker, unable to find its script:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">/usr/libexec/gcc/avr/ld: cannot open linker script file ldscripts/avr5.x: No such file or directory
</pre>

This is [Gentoo bug #147155](http://bugs.gentoo.org/show_bug.cgi?id=147155), which at the moment is not fixed.  The workaround:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">ln -s /usr/lib/binutils/avr/2.20/ldscripts /usr/avr/lib/ldscripts
</pre>

And finally, we have a build:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">dustin@erdos ~/tmp/Blink $ make
# Here is the "preprocessing".
# It creates a .cpp file based with the same name as the .pde file.
# On top of the new .cpp file comes the WProgram.h header.
# At the end there is a generic main() function attached.
# Then the .cpp file will be compiled. Errors during compile will
# refer to this new, automatically generated, file.
# Not the original .pde file you actually edit...
test -d applet || mkdir applet
echo '#include "WProgram.h"' &gt; applet/Blink.cpp
cat Blink.pde &gt;&gt; applet/Blink.cpp
cat /usr/share/arduino-0017/hardware/cores/arduino/main.cxx &gt;&gt; applet/Blink.cpp
/usr/bin/avr-gcc -mmcu=atmega168 -I. -gstabs -DF_CPU=16000000 -I/usr/share/arduino-0017/hardware/cores/arduino -Os -Wall -Wstrict-prototypes -std=gnu99  -o applet/Blink.elf applet/Blink.cpp -L. applet/core.a -L/usr/avr/lib -lm
cc1plus: warning: command line option "-Wstrict-prototypes" is valid for Ada/C/ObjC but not for C++
cc1plus: warning: command line option "-std=gnu99" is valid for C/ObjC but not for C++
/usr/bin/avr-objcopy -O ihex -R .eeprom applet/Blink.elf applet/Blink.hex

   text    data     bss     dec     hex filename
      0    1244       0    1244     4dc applet/Blink.hex
</pre>

running <tt>make upload</tt> as root, right after pressing the reset button in the board, successfully uploads the program.  Blinkies!

## Cleanup

A few
 small changes will make a lot of this easier.  First, I want to make 
sure that the USB device is writable by a non-root user, using udev.  
First, I used the following command to get the udev identifying 
information for the device.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">udevadm info --attribute-walk -n /dev/ttyUSB0
</pre>

The 
identifiers for the device are given from most-specific to 
least-specific.  The device itself doesn't have much to identify it:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">  looking at device '/class/tty/ttyUSB0':
    KERNEL=="ttyUSB0"
    SUBSYSTEM=="tty"
    DRIVER==""
</pre>

but I need something to match on this device, so I used <tt>SUBSYSTEM=="tty"</tt>.  To avoid confusion with other tty devices, though, I needed something more specific.  Looking at the parent entry, I see

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">    ATTRS{interface}=="FT232R USB UART"
</pre>

which looks like a good identifier for this component.  Aside from setting the ownership and permissions, I decided to add a <tt>/dev/avr</tt> symlink, too.  The completed rule is:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001" GROUP="users", MODE="0666", SYMLINK+="avr"
</pre>

The first three fields match the device using the numbers from <tt>lsusb</tt>, and the last three set the proper group-id, mode, and dev-tree symlink for the device.  I put this rule in <tt>/etc/udev/rules.d/10-user.rules</tt> and updated udev:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">udevadm trigger
</pre>

sure enough, <tt>/dev/avr</tt> now exists.  I added this path as the <tt>PORT</tt> in the Makefile.

The 
second problem is that the makefile is not smart enough to reset the  rewrite](http://code.v.igoro.us/archives/12-Perl-vs.-Python.html).  But it's too late now!

Second, and more importantly, Perl code can be hacked in place.  If [amvault](http://wiki.zmanda.com/man/amvault.8.html) isn't acting the way you want it to, just open up <tt>/usr/sbin/amvault</tt>
 and tweak away.  No need to download the source, no need to compile, no
 segmentation faults, just hacking.  When you're done, run a quick <tt>diff</tt> and send the results to amanda-hackers.

Even users who do not know Perl can take advantage of this _in-situ_
 hackability.  Within Amanda's C code, if I want a user to try a patch, 
that user must figure out how to download Amanda's source, apply the 
patch, configure, compile, and install.  None of those steps are 
trivial.  With Perl code, I can often provide a patch that is simple 
enough to be applied directly to the installed executables by hand, or 
with a simple application of <tt>patch</tt>.  Everyone stays focused on the bug under investigation, and the user's backups are up and running that much more quickly.

# New APIs

As I 
mentioned before, historically Amanda's code has been highly 
interdependent.  Details of the implementation of the holding disk were 
spread over most of the files in the server implementation.  The 
dumplevel -987 has a special meaning that is documented nowhere, but 
referenced in several source files.  All of this makes new development 
difficult, because it's impossible to "slice off" and study a portion of
 Amanda in isolation.

The 
solution here is to create abstract interfaces, where new functionality 
can be "plugged in" and Amanda can use it without changes.  The Amanda 
developers have abused the term "API" for these interfaces, and we now 
have quite a few:

*   [Application API](http://wiki.zmanda.com/index.php/Application_API) - an abstraction of backup clients, e.g., [ampgsql](http://code.v.igoro.us/archives/50-Whats-New-in-Amanda-Postgres-Backups.html) for Postgres;

*   [Device API](http://wiki.zmanda.com/index.php/Device_API) - an abstraction of backend storage devices, such as tape, disk, cloud, or DVD-RW;

*   [Changer API](http://wiki.zmanda.com/index.php/Changer_API) - an abstraction of tape changers and other mechanisms for selecting from a set of volumes; and

*   [Script API](http://wiki.zmanda.com/index.php/Script_API) - a means of invoking scripts before or after certain events during a backup.

This 
strategy has already paid off: we have seen several new scripts and 
applications contributed, and the DVD-RW device arrived out of the blue 
as a contribution from someone who found it useful.

# Other Changes

In the interest of greater accessibility to new hackers, we have also put Amanda on [github](http://github.com/zmanda/amanda) and created a set of good "beginner" projects.  Zmanda has even offered to [pay people to hack on Amanda](http://code.v.igoro.us/archives/53-Want-to-work-on-Amanda.html),
 as a way of easing the cost of entry.  I also try to point out 
interesting projects on the Amanda mailing list, particularly projects 
that Jean-Louis and I probably will not find time to work on.

The 
idea here is to encourage new hackers to pick up a well-scoped project 
to become familiar with Amanda.  The hackers can then move on to more 
sophisticated projects that meet their particular backup needs or 
address a particular interest.

# Will You Join Me?

So Amanda is ready for you.  When can you start?
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">What's New in Amanda: Transfer Architecture</span>](http://code.v.igoro.us/archives/49-Whats-New-in-Amanda-Transfer-Architecture.html)<div class="lastUpdated">March 12, 2010 3:06 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

Amanda's
 primary mission in life is to move large quantities of data around.  
Historically, this has been done through a patchwork of methods, each 
written separately and with its own quirks.  POSIX p V+ to the **3.3V pin**
 on the Arduino (the device is only specified for 3.6V) and GND to the 
TMP102's GND.  Finally, the TMP102's ADD0 pin can cleverly select one of
 four addresses for the device by tying it to one of these four pins.  I
 tied it to GND, giving address 0b1001000.  ALARM is an output pin, so 
you can leave it unconnected.

The 
TMP102 is a very nice low-power device that's designed to handle several
 common tasks without any interaction from the MCU - it can trigger an 
interrupt when the temperature strays from a configured boundaries, poll
 temperature on a relatively slow schedule, or even poll on command.  I 
didn't use any of that, relying on the device to simply sample the 
temperature on its own schedule.

The 
TMP102 has four registers, but we'll only use one -- temperature (0b01).
  Like many devices, this one multiplexes addresses and data over the 
same bus.  To read a register, you first select the register by writing 
it to the device, then read the 16-bit value, again with the MSB first. 
 Once a register is selected, it can be read multiple times.

The 
device's temperature register contains a two's-complement 12-bit value, 
left-aligned, where 0x7FF is 128°C; equivalently, a change of one unit 
in the 12-bit value is equivalent to 0.0625°C.

## Putting it Together

The obvious combination of these tools is to display the ambient temperature on the LCD screen.  Here's the program to do so:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">#include &lt;Wire.h&gt;
#include &lt;LiquidCrystal.h&gt;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2); 

#define TEMP_REG 0b00000000
int tmp102 = 0b1001000;  // with ADD0 tied to ground

void setPR(int reg) {
  Wire.beginTransmission(tmp102);
  Wire.send(reg);
  Wire.endTransmission();
}

int getReg() {
  unsigned char lo, hi;

  Wire.requestFrom(tmp102, 2);
  hi = Wire.receive();
  lo = Wire.receive();
  return (hi &lt;&lt; 8) + lo;
}

void setup()   {    
  lcd.begin(16, 2);
  Wire.begin();
  setPR(TEMP_REG);
}

void show_temp() {
  int temp_reg = getReg();
  lcd.setCursor(0, 0);
  show_bin(temp_reg);

  temp_reg &gt;&gt;= 4;

  float temp_C = temp_reg * 0.0625;
  float temp_F = (temp_C * 9 / 5) + 32;

  lcd.setCursor(0, 0);
  lcd.print(temp_C);
  lcd.print("\xdf""C  ");
  lcd.setCursor(0, 1);
  lcd.print(temp_F);
  lcd.print("\xdf""F  ");
}

void loop() {
  show_temp();
}
</pre>

The <tt>setup</tt> function sets up the LCD, then uses <tt>setPR</tt> to point the TMP102 at the temperature register.  Subsequent reads will then return the 12-bit encoded temperature.  The <tt>loop</tt> function reads the temperature register, decodes it, and displays the result in both Celsius and Fahrenheit.

Note that this is horrendously inefficient: the TMP102 only measures temperature every 26ms or so, during which <tt>loop</tt>
 will probably run a half-dozen times, feeding the same time strings to 
the LCD each run.  It would be much better to put the TMP102 in one-shot
 mode, and measure the temperature at a much lower frequency - say once a
 second - with a correspondingly low update frequency for the display.  
I'll leave that as an exercise for the reader.
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">IPv6 Configuration</span>](http://code.v.igoro.us/archives/57-IPv6-Configuration.html)<div class="lastUpdated">June 27, 2010 5:27 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent"><div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">[![IPv6 Certification Badge for djmitche](codevigorous_files/create_badge.png)](http://ipv6.he.net/certification/scoresheet.php?pass_name=djmitche)</div>I've been meaning to get IPv6 set up on my local network for some time.  My only practical reason is that [Amanda](http://amanda.org/)
 supports IPv6 and I should test that support.  It was also a good 
chance to re-immerse myself in network configuration, and Hurricane 
Electric has a neat [certification pronot known in advance what sort of address they will
 contain.  We added a set of macros and utility functions in [sockaddr-util.c](http://github.com/zmanda/amanda/blob/master/common-src/sockaddr-util.c) and [sockaddr-util.h](http://github.com/zmanda/amanda/blob/master/common-src/sockaddr-util.h).
  Using these macros throughout Amanda removed a significant amount of 
code that was conditionalized on both compile-time support and runtime 
address family, and centralized that logic in one easily-maintained 
place.

On 
our build systems, we had to deal with different levels of support in 
the compile environment and the kernel.  This is fine: most Amanda users
 install binary packages that are produced on roughly the same OS 
distribution and version as was used for the build, so the kernel 
support is generally the same.  However, a third variable has tripped up
 lots of Amanda users: system configuration.  In particular, several 
newer Linux distributions have shipped with <tt>localhost</tt> resolving to ::1 vi <tt>/etc/hosts</tt>,
 but without enough interface configuration to actually utilize a socket
 bound to that address.  Amanda uses localhost sockets for inter-process
 communication, so this misconfiguration causes backup operations to 
fail.  The solution is to either finish configuring IPv6 on the host, 
remove the reference to ::1 in <tt>/etc/hosts</tt>, or build Amanda with <tt>--without-ipv6</tt>.

I 
have not yet heard of an Amanda installation where IPv6 communication is
 in use.  But I have heard from countless IPv4 users whose Amanda 
installations have failed due to bad IPv6 support.  At the moment, then,
 I feel that adding IPv6 support to Amanda has been a net negative for 
the project.  Although there is doubtless room for improvement, I will 
not entertain patches for better IPv6 support, for fear they will 
introduce new bugs for our exclusively IPv4 userbase.

Of course, all of this may change as dual-stack networks grow more prevalent and are replaced by pure IPv6 networks!
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">irssi settings for status-in-nick</span>](http://code.v.igoro.us/archives/63-irssi-settings-for-status-in-nick.html)<div class="lastUpdated">October 22, 2010 1:06 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

I
 am getting started in releng at Mozilla, and IRC provides a central 
meeting-place for the group.  As such, indicating your status to this 
group is an important, so others can know whether you're nearby to 
answer a question or take care of a problem.  This is generally done by 
adding suffixes to the IRC nickname, e.g., "dustin|afk" or 
"dustin|lunch".

Before
 I go further, I know that this is frown on, and even results in 
autoignores, in some corners of IRC.  If that's the case for you, read 
no further. [Irssi](http://irssi.org/)'s documentation is 
utterly incomplete.  So the only way to figure out how to configure 
something or write a script is to find and adapt examples.  So hopefully
 this entry will feed back into that pool.

What I want is an easy way to bind some keystrokes to commands like <tt>/NICK dustin|afk</tt>.  However, I want to be very careful _not_
 to set this nick on other chatnets, particularly since I'm generally 
known as djmitche there, not dustin.  So I began by writing a script 
that can double-check this:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">use strict;

use vars qw ($VERSION %IRSSI);

$VERSION = 'v1.0';
%IRSSI = (
          name        =&gt; 'moznick',
          authors     =&gt; 'dustin',
          contact     =&gt; 'dustin@mozilla.com',
          url         =&gt; 'http://code.v.igoro.us/',
          license     =&gt; 'GPLv2',
          description =&gt; 'Sets my nick status for Mozilla co-workers',
         );

use Irssi;

my $last_nick = '';

sub is_mozilla {
    my ($server) = @_;
    if (!$server || $server-&gt;{'chatnet'} eq 'mozilla') {
        return            
      +-puppetmaster2 CA--+-puppetmaster2 server cert
                          |
                          +-client 10 server cert
                          :
</pre>

Then 
all of the certificate validation would be done with the root CA 
certificate as the trusted certificate.  A server certificate signed by 
puppetmaster2's CA cert should then validate on puppetmaster1.

Building the certificates wasn't all that difficult - see [my comment on the bug](https://bugzilla.mozilla.org/show_bug.cgi?id=733110#c8)
 for the script.  However, while making sure the verification worked, I 
ran into some non-obvious limitations of OpenSSL that are worth writing 
down.

I began by running "openssl verify":

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">[root@relabs-puptest1 ~]# openssl verify -verbose -CAfile puptest-certs/root-ca.crt -purpose sslclient puptest-certs/relabs08.build.mtv1.mozilla.com.crt 
puptest-certs/relabs08.build.mtv1.mozilla.com.crt: CN = relabs08.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
error 20 at 0 depth lookup:unable to get local issuer certificate
</pre>

the 
problem here is that the intermediate certificate is not available to 
the verification tool.  Sources suggest to include it with the server 
cert, by concatention, with the server cert last:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">cat puptest-certs/relabs-puptest1.build.mtv1.mozilla.com-ca.crt puptest-certs/relabs08.build.mtv1.mozilla.com.crt &gt; relabs08-with-intermed.crt
</pre>

However,
 after some struggle I learned that "openssl verify" does not recognize 
this format -- it will only look at the first certificate in the file 
(the intermediate), and if you don't look carefully you'll find that it 
successfully verifies the intermediate, not the server certificate!  
Sadly, s_client and s_sever don't support it either.  Apache httpd supports it with [SSLCACertificatePath](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcacertificatepath).
  This will feed the certificate chain to the client, and also allow 
httpd to verify client certificates without requiring the clients to 
support an intermediate.

The Apache config is

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Listen 1443

&lt;VirtualHost *:1443&gt;
        ServerName relabs-puptest1.build.mtv1.mozilla.com
        SSLEngine on
        SSLProtocol -ALL +SSLv3 +TLSv1
        SSLCipherSuite ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM:-LOW:-SSLv2:-EXP

        SSLCertificateFile /etc/httpd/relabs-puptest1.build.mtv1.mozilla.com.crt
        SSLCertificateKeyFile /etc/httpd/relabs-puptest1.build.mtv1.mozilla.com.key
        SSLCACertificatePath /etc/httpd/ca-path

        # If Apache complains about invalid signatures on the CRL, you can try disabling
        # CRL checking by commenting the next line, but this is not recommended.
        #SSLCARevocationFile     /etc/puppet/ssl/ca/ca_crl.pem
        SSLVerifyClient require
        SSLVerifyDepth  2

&lt;/VirtualHost&gt;
</pre>

While
 you're getting that set up, you're probably wondering where to get this
 fancy "c_rehash" utility.  Don't bother.  It's about as simple as:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">for i in *.crt; do
        h=`openssl x509 -hash -noout -in $i`
        rm -f $h.0
        ln -s $i $h.0
done
</pre>

As a side-note, the results of verification by s_client and s_server
 are not very obvious.  Look for the overall error message near the 
bottom of the output.  Here's the result of a client verification once I
 had everything put together, with some long uselessness elided:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">[root@relabs-puptest1 ~]# openssl s_client -verify 2 -CAfile puptest-certs/root-ca.crt -cert puptest-certs/relabs08.build.mtv1.mozilla.com.crt -key puptest-certs/relabs08.build.mtv1.mozilla.com.key -pass pass:clientpass -connect localhost:1443
verify depth is 2
CONNECTED(00000003)
depth=2 CN = PuppetAgain Roduring most of that startup time, it has a blank 
screen with no backlight, and sometimes startup crashes, so it's a bit 
of a psychological game to resist popping out the battery early.

Fine,
 so it starts up, I start the navigation application, and hit "Go Home".
  It plots a route, I take off, get on the highway, and the phone dies. 
 At this point I do the math -- if my phone went from 100% to 10% in 6 
hours while navigating, then it requires the combined power of both the 
battery _and_ the adapter to run the navigation app.  So I 
dutifully hand the phone to S to start back up and hit the "Go Home" 
button again.  I immediately turn off the backlight and hope for the 
best.  The navigation voice tells me to head South for 40 miles, and 
then I hear nothing.

This 
should have been a red flag, but I was too busy composing this blog 
entry in my head to do a little more arithmetic: Albany is not South of 
New Haven.  A half-hour later, S checked her iPhone and pointed out we 
were heading the wrong direction.

I 
pulled over and checked my phone.  Surprisingly, it was still on!  
However, it was navigating to Waters View, NY, which is not where we 
live.  We live at  Waters View Circle, Cohoes, NY.  Google knows this.  
It's set in the navigation app.  It turns out that Google takes the 
string you type in for your home address and hits the API equivalent of 
the "I'm feeling lucky" button, and you're off to the races.  Perhaps 
not the races you were looking for.  This is the same fundamental flaw 
as plagues Google Now.  If you're in, say, Springfield, MA, but for 
whatever reason the location-aware "I'm feeling lucky" feels 
Springfield, IL is the more relevant search result, you get Springfield,
 IL's  weather.  And it helpfully just says "Springfield" on the card, 
so you don't know anything's wrong until it claims there's torrential 
rains on a clear day.

At 
this point we killed my phone and navigated the old-fashioned way - 
getting directions on the iPhone and following the relevant signs.  It 
turns out we had a great drive along the Taconic State Parkway, which is
 a far sight more interesting than I-90, so that was OK.  And we only 
lost an hour of drive-time.

Aside
 from the battery-life issues, which are not surprising from Samsung, 
but are surprising from a phone with "Google" on the back, there's an 
important point here: Google's approach to problems is to throw 
gargantuan amounts of data and CPU at them, and hope the answer's right.
  That's fine for search, but when it comes down to building a reliable 
personal device, people need something a little more deterministic.  
Google is increasingly heading toward personalized computing -- Google 
Glass being the ultimate expression -- and I think the company has a lot
 to learn before any of that will be more than an amusingly daft 
automaton. 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Documentation for MDT's CustomSettings.ini</span>](http://code.v.igoro.us/archives/78-Documentation-for-MDTs-CustomSettings.ini.html)<div class="lastUpdated">October 25, 2012 11:59 AM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

If
 you're looking for info on CustomSettings.ini, you're most likely to 
find questions answered with "try this script".  You type it in, and if 
it works, great; if not, keep looking.  It's well-nigh impossible to 
find actual documentation, and the programming-by-INI-sections design is
 not exactly intuitive.

It 
turns out there's some in the help docs for the MDT, but those are a 
.CHM file and Microsoft apparently doesn't post those online.  

However, some helpful (Russian?) souls have done so.  Behold: [Microsoft® Deployment Toolkit 2012 Toolkit Reference](http://systemscenter.ru/mdt2012.en/toolkitreference.htm). 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Locking SSH keys on sleep on Linux</span>](http://code.v.igoro.us/archives/79-Locking-SSH-keys-on-sleep-on-Linux.html)<div class="lastUpdated">March 29, 2013 12:42 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

I
 got a new laptop, a ThinkPad X1 Carbon, and I'm running Linux on it.  
So you're in for a series of posts describing the complex process I had 
to follow to accomplish simple things.  Spoiler alert: 2013 is not the 
year of Linux on the desktop.  It's not looking good for 2014 either.

I'm 
running Fedora 18.  I tried Ubuntu 12.10, but Unity couldn't hold itself
 together long enough to actually do anything, so I started over with 
Fedora.

## SSH Agent

Gnome runs a nice keychain app that acts like (but is not) OpenSSH's ssh-agent.  The one obvious place it differs is that <tt>ssh-add -l</tt> will list keys even if they are "locked" (passphrase not supplied).

As long as you point the SSH_AUTH_SOCK variable to the right place, the agent works just fine for unlocking keys - it finds any private/public pairs in <tt>~/.ssh</tt>, and prompts to unlock them once you issue an SSH command that needs a key.  The problem is, it never re-locks the keys.

## Locking

Personally,
 I use SSH constantly while my laptop is awake, so I don't want an 
arbitrary timeout.  Instead, I'm careful to put it to sleep when I'm 
away from the keyboard.  So I want a way to lock the key on sleep.

It 
turns out that pm-utils will run scripts in /etc/pm/sleep.d on sleep and
 wake.  It runs them as root, unfortunately.  I added the following in <tt>01dustin-ssh-agent.sh</tt>:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">#!/bin/sh

# drop keys from dustin's SSH agent

. "${PM_FUNCTIONS}"

lock()
{
        su - dustin /home/dustin/bin/ssh-lock
}

case "$1" in
        hibernate|suspend) lock ;;
        *) exit $NA ;;
esac
</pre>

and then added the following in <tt>~/bin/ssh-lock</tt>:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">#!/bin/sh

# drop keys from the SSH agent, using the same trick as bin/startscreen to find
# that agent

base="/tmp"
[ -d /run/user ] &amp;&amp; base="/run/user/$(id -u)"
socket_dir="$base/$(uname -n)-$(id -u)"
SSH_AUTH_SOCK=$socket_dir/agent ssh-add -D
</pre>

See [my post](http://code.v.igoro.us/archives/60-SSH-With-Snow-Leopard.html)
 on tunneling ssh-agent into a screen session for the reference to 
bin/startscreen.  I'm not sure how best to accomplish this without such a
 trick.  I'll work on that and post again. 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">910 Days at Mozilla</span>](http://code.v.igoro.us/archives/80-910-Days-at-Mozilla.html)<div class="lastUpdated">April 15, 2013 2:26 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

As
 of today, I've been at Mozilla for 910 days.  That's not a magic 
number, but this seemed like a good day to reflect on my time here.

I've had a chance to do a bunch of exciting things here:

*   Drink from the Mozilla Firehose

*   Manage build slaves in the release engineering environment

*   Build out a configuration management system with Puppet

*   Design systems to build out new hardware platforms and operating systems

*   Organize a move of systems and servers out of one datacenter and into another.

*   Build a web cluster

*   Build and maintain MySQL database clusters as an apprentice DBA

*   Learn Ruby and hack on Puppet

*   Build a dynamic hardware provisioning system ([Mozpool](https://github.com/mozilla/mozpool))

You'll
 never be bored at Mozilla!  There's never a shortage of work to do, 
with new projects coming all the time.  The organization is structured 
so that it's easy to take on tasks that need doing, whether they're 
within your skill base or not.  There's lots of room to learn, and 
everyone's happy to teach.

I 
work with an incredible group of people.  Just within IT, we have a huge
 range of skills and capabilities for a relatively small team.  People 
who know how to _really_ solve problems, not the half-baked 
temporary solutions that you find elsewhere.  As but one example, the 
datacenter operations team is building out and operating several 
world-class datacenters at the same time, and still managing to turn 
around our remote-hands requests in matters of hours.  Our 
infrastructure team is full of people with deep experience in all 
aspects of system administration who are always willing to help solve a 
tricky problem.  And on my own team, my co-workers all manage to work 
miracles far beyond the resources available.

Before
 Mozilla, I was at Zmanda, working on Amanda -- you know, the 
open-source backup application you remember from your early days?  It's 
still around!  Anyway, I took that job in part because it meant I could 
be paid to work on open-source software.  I took full advantage of that 
opportunity, but the company was fundamentally a company - organized 
around sales, support, and the bottom line.  My open-source concerns 
always played second fiddle, if that.  Mozilla's different: the [Mozilla Manifesto](http://www.mozilla.org/about/manifesto.en.html) is _what we do_,
 and that's understood nowhere better than at the top of the 
organization.  It can be a struggle sometimes, to see how the work I do 
supports the people who support the people who build the products that 
further the mission, but the connection is there and it's important.  
That keeps me going.

Here's to another 1000 successful days at Mozilla! 
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Oops, I partitioned my drive..</span>](http://code.v.igoro.us/archives/81-Oops,-I-partitioned-my-drive...html)<div class="lastUpdated">May 29, 2013 2:48 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

I
 did something colossally stupid yesterday.  I was at the local 
hackerspace, hoping to cut some acrylic, and the wifi wasn't working.  I
 was in a hurry and frustrated, so I pulled out a USB stick and tried to
 erase it.  Suffice to say, the USB stick wasn't at <tt>/dev/sda</tt>.  I
 wiped out the GPT on my laptop.  Its disk is encrypted, so the buffer 
store kept things working for a while, then suddenly I had a blinking 
root prompt and .. nothing.

After
 the obligatory cold-sweat had passed, I quietly packed up and walked 
out.  Here's the story of how I recovered from this, with the help of 
Jake Watkins (:dividehex). The system didn't have any irrecoverable data
 on it.  All of my work is in version-control, and I'm religious about 
pushing to github.  Even my home directory's dotfiles are on github (in a
 private repo).  But I spent several weeks setting this laptop up (Linux
 on the desktop is only usable from a very long-term perspective!), and 
unfortunately one of the few things that wasn't in version control was 
my notes on how I'd done so.  Rebuilding this from scratch would take a 
few weeks and make a very grumpy Dustin.

To 
make things interesting, this ThinkPad X1 Carbon has no Ethernet port.  
It's wifi only.  There are dongles available from Lenovo, but I don't 
have one.

## Backup

OK, so let's stop the bleeding.

I 
booted from the Fedora Live USB stick I'd used to install the system 
initially.  Once it was up, I schlepped the entire drive over to my 
desktop:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">ssh root@ramanujan dd if=/dev/sda &gt; laptop-disk.img
</pre>

That 
took about 8 hours, but that gave me time to do some other research, 
conduct a Baltic Porter tasting (multitasking!), and sleep.

## Find the Data

So 
the situation is that I have a partition table with a single 256G FAT32 
partition in it.  Somewhere on the disk, my data is probably still 
intact.  But where?

Jake suggested looking for the GPT backup table, which is at the end of the disk.  The <tt>gdisk</tt> advanced options allow you to examine this table, but it too was empty.

Jake's other suggestion was to look for the signature of the LUKS crypto container.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">dd if=/dev/sda | od -c | grep 'L   U   K   S'
</pre>

This 
eventually turned up the beginning of the partition, 05364000000 
(decimal 735051776) bytes into the disk.  Dividing that by 512, the size
 of a sector, that's sector 1435648.

In <tt>gdisk</tt>, I created a partition beginning at that location and running to the end of the disk.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1"># cryptsetup luksDump /dev/sda1
LUKS header information for /dev/sda1

Version:        1
Cipher name:    aes
Cipher mode:    xts-plain64
Hash spec:      sha1
Payload offset: 4096
MK bits:        512
MK digest:      e2 f9 fa 7d 44 dc 82 f5 3c 39 1d e2 ac 6e e3 d2 d0 f5 2b 1b 
MK salt:        05 8b a0 ee 7a bf 37 73 7b 15 c1 7a 41 0b 46 19 
                56 68 e1 36 f7 7c b3 d0 74 bf 21 98 a1 e6 75 7b 
MK iterations:  13750
UUID:           4057691b-b580-4d05-afd3-9e2efe8d65d3
...
</pre>

so it looks like I've found the data.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1"># cryptsetup luksOpen /dev/sda1 secret

# mount /dev/mapper/secret /mnt
</pre>

This 
didn't work.  It's not an ext4 volume - it's an LVM physical volume.  
Udev has already run the pvscan, so I just need to activate the volume 
group:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1"># vgscan -a y fedora
# mount /dev/fedora/root /mnt
# mount /dev/fedora/home /mnt/home
</pre>

At 
this point, it's time for another backup.  I used tar to dump the 
contents of both partitions, storing the tarball on my desktop machine. 
 This took about an hour.  Now I feel a lot better -- I have my notes 
from customizing the system, and anything else that's not backed up that
 I might have forgotten.  But I haven't actually lost any data - can I 
recover this completely?

## Rebuild It

I 
reboot the Live USB stick, just to reset all of the partition maps, luks
 opens, etc. that I had done.  I realize that /dev/sda1 is probably not 
the right partition number for the full filesystem, so I move that to 
/dev/sda3 (by deleting and re-creating with the same first/last 
sectors).  Another reboot.

When it starts up again, I fire up the installer and tried to install _around_
 the existing data.  I figure I can do a minimal installation in some of
 the free space, particularly since Anaconda reassured me that it only 
needed 3.1G.  

Long 
story short, this was a lie.  Anaconda is a horrible piece of software, 
with bugs galore.  For example, if you set a partition's size, it will 
randomly make up another size and use that instead.  Ugh.

It 
turns out, Anaconda needs about 15G to do the install.  So, I need to 
shrink /dev/sda3 by at least that much.  I resize logical volumes all 
the time, but this is the reverse -- I need to shrink a physical volume.
  That turns out to be a bit tricky.  First, after opening the LUKS 
volume, I run <tt>pvresize</tt>:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">pvresize --setphysicalvolumesize 210g /dev/mapper/secret
</pre>

This 
fails, telling me that there are extents beyond the new last extent.  
Subtract a few from that last extent and call that $boundary.  Run <tt>pvdisplay /dev/mapper/secret</tt> to get the total physical extents, and call that $total.  Then, use <tt>pvmove</tt> to shift those around:

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">pvmove --alloc anywhere /dev/mapper/secret:$boundary-$total /dev/mapper/secret:0-$boundary
</pre>

and I re-run the <tt>pvresize</tt> command.

Now, I
 resize the LUKS container that PV is housed in.  This requires a little
 arithmetic.  LVM uses "GiB", which are the normal power-of-two things, 
not the stupid disk-manufacturer power-of-ten things.  So 210g is 
225485783040 bytes, which (divided by 512) is 440401920 sectors.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">cryptsetup resize --size 440401920 /dev/mapper/secret
</pre>

OK, I
 shrank the PV, I shrank the enclosing LUKS container, and now I need to
 shrink the partition.  This means deleting and re-adding the partition 
in gdisk.  The starting sector stays the same, while the last sector is 
calculated as $starting_sector + 440401920 - 1.  The -1 is important 
there - I'm specifying the _last_sector, not the first sector of 
the next partition.  That'd be a sad way to lose 512 bytes of data when I
 least expect it.  The filesystem type doesn't seem to matter - I used 
the default, but I noticed that Anaconda uses 0700.

Reboot
 and run the install again.  Let Anaconda do its thing, because it's not
 going to listen to me if I try to customize it.  Anaconda happened to 
choose a different VG name (fedora_ramanujan) for the new volume group. 
 If it hadn't, I might have had to rename things.  Reboot, and I have a 
fresh system.

If I was smart, I would have run 'yum upgrade' now, but I didn't.  More on that in a second.

The 
idea is that I now have UEFI set up, and all of the proper boot 
partitions, but it's running from the wrong encrypted partition.  
Changing that is as simple as editing /boot/efi/EFI/fedora/grub.cfg, 
replacing the new VG name with the old VG name, and the new LUKS UUID 
with the old LUKS UUID (from 'cryptsetup dumpLuks').  Reboot, enter my 
passphrase, and .. "Welcome to emergency mode!".  A bit of poking around
 shows that all of my partitions are mounted properly, but the journal 
shows failures mounting /boot/efi, because of a missing vfat module.

## Kernel Woes

The kernel and initrd are, of course, on /boot, and are the version installed from the Live USB stick.  The kernel _modules_ are on /, and are the updated versions from several months later.  They don't match up.

The 
quick fix is to mount the new LUKS container and copy /lib/modules over 
/lib/modules on the old container.  This gets me a copy of all of the 
modules that Anaconda had installed, and lets me boot all the way into a
 working system .. almost.  The wifi isn't working.

This 
is probably because I'm running an old kernel version with an 
otherwise-updated system.  Upgrading to the latest kernel is the fix.  
That's tricky with no wifi, so I look up the packages on my desktop, 
throw them on a USB stick (being very careful not to re-partition my 
desktop's HDD in the process!), and run

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">yum reinstall /mnt/usb/kernel-*
</pre>

on the laptop once the USB stick is mounted there.  Reboot, and all is back to normal.

That was not the most fun I've ever had in 20 hours.  But it was an adventure.
</div></div><div style="clear: both;"></div><div class="entry">

### [<span xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">Threading an SSH Agent Through Screen</span>](http://code.v.igoro.us/archives/82-Threading-an-SSH-Agent-Through-Screen.html)<div class="lastUpdated">November 6, 2013 12:13 PM</div>
<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">

_I
 posted this three years ago, buried in an unrelated post, but several 
people have asked me about it lately, so here it is in a dedicated post._

You 
should only have your SSH private key on hosts that are physically in 
your posession - laptop, desktop, etc.  But you usually want to put 
those hosts to sleep or move them around, which means they can't keep 
live SSH connections going in a screen session.  So you probably run 
screen on a server somewhere - a VPS, an admin host at work, or if 
you're like me, a server in your basement.

Now 
you have a new problem: when you first start the screen session, your 
SSH agent works fine in screen windows.  But when you disconnect and 
reconnect, all of those screen windows are still looking for the old SSH
 agent, which no longer exists.  So SSH connections in a reconnected 
screen session fail.

Well,
 there's a fix!  The idea is to mirror the auth socket to a well-known 
name that is stable from one SSH connection to the next.

<pre xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1">#! /bin/bash
# hard-link the SSH socket to one with a fixed name on the local
# machine, and set SSH_AUTH_SOCK to point to that fixed name.  Later
# invocations of this script will change the link, but the name will
# remain valid, allowing existing shells to continue to function.
setup_fixed_socket() {
  local old_socket="$SSH_AUTH_SOCK"
  local socket_dir="/tmp/$(uname -n)-$(id -u)"
  local socket_file=$socket_dir/agent

  # set up the directory and permissions
  [ -e $socket_dir ] || mkdir -p $socket_dir
  chmod 700 $socket_dir

  # remove an existing link
  [ -e $socket_file ] &amp;&amp; rm $socket_file

  # hard-link in the new one
  ln $old_socket $socket_file

  # return the new socket
  echo $socket_file
}

# this variable will be exported to every shell opened by this
# invocation of screen -- even subsequent connections to it.  This
# variable may live for days or weeks.
export SSH_AUTH_SOCK=$(setup_fixed_socket)

# finally, fire up screen.  Try reattaching to a running
# session; otherwise start up a new one
screen -R -DD ${@} || screen
