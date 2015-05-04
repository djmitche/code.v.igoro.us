---
layout: post
title:  "HG Workflow"
date:   2015-05-04 12:00:00
---

I'll admit it, I'm a big fan of Git.
I find its model to be simple and powerful.
It's extremely flexible, and extremely fast.
Conversely, I find Mercurial to be slow and far too opinionated.
Its prohibition on editing history is easy to overcome by blowing away the local repository and re-cloning, then applying the old patch.
I know because I have used this technique many times.

Mozilla uses Mercurial for much of its work, notably the [Firefox source code (Gecko)](https://hg.mozilla.org/mozilla-central/), and a few projects I work on - [PuppetAgain](https://hg.mozilla.org/build/puppet/), [Mozharness](https://hg.mozilla.org/build/mozharness), and the vaguely-named and vaguely-defined [Tools](https://hg.mozilla.org/build/tools/) to name a few.
For the last few years, I've accessed these repositories via [git-remote-hg](https://github.com/felipec/git-remote-hg), a "bridge" allowing me to push from a local Git repository to a remote Mercurial repository.
This tool has had a lot of issues, though, many involving severe repository corruption.
There's work afoot to build a better, more compatible version, but after conversations with Gregory Szorc a few weeks ago, I determined to make the effort and give Mercurial a fair shake.

The rest of this post outlines my approach, as usual as much for my reference as for yours.

## Repository Setup

I have a single local repository for each codebase, as shown above.
Mercurial doesn't have the nice `git config` interface, so you need to set the repository up by grubbing around in `.hg`, mostly in `.hg/hgrc`.

### Extensions

All of the good stuff in Mercurial is in extensions.
Fortunately, most of them are built in.
Here's the list of those built-in extensions:

    [extensions]
    color =
    rebase =
    purge =
    histedit =
    record =
    pager =
    shelve =
    progress =
    graphlog =

I'll talk more about the functionality these afford below.

### Mozilla-Specific Extensions

There are a few fantastic extensions written specifically to interact with Mozilla stuff.
These are in the https://hg.mozilla.org/hgcustom/version-control-tools repository.
To set this up (assuming the extensions are the last thing listed in your hgrc):

    cd .hg
    hg clone https://hg.mozilla.org/hgcustom/version-control-tools
    echo firefoxtree = $PWD/version-control-tools/hgext/firefoxtree >> hgrc
    echo reviewboard = $PWD/version-control-tools/hgext/reviewboard/client.py >> hgrc

Unfortunately those need to be absolute paths.
The firefoxtree extension is only useful for Gecko.

### Identity

I added the following.  You'll want to use something slightly different:

    [ui]
    username = Dustin J. Mitchell <dustin@mozilla.com>

### Ignoring local files

I generally have a virtualenv or some other stuff in my working copy that I don't want versioned, but which is too specific to my use-case to commit to the versioned `.hgignore` file.
In Git, such files are simply added to `.git/info/exclude`, but in Mercurial you'll need to set up an ignore file, again with a full path:

    [ui]
    ignore = /path/to/repo/.hg/hgignore

Then list the ignored files, noting that Mercurial uses regular expressions, in `.hg/hgignore`.

### Diff Improvements

Mozilla has a [preferred diff configuration](https://developer.mozilla.org/en-US/docs/Mercurial_FAQ#Interactive-hg-setup):

    
    [diff]
    git = 1
    showfunc = 1
    unified = 8

### Reviewboard Setup

Reviewboard will need your IRC nick for pushing review requests:

    [mozilla]
    ircnick = dustin

### Paths

I like to set my default path to point to my "public" repository (I use bitbucket because there's [a bug with Mozilla's user repo hosting](https://bugzilla.mozilla.org/show_bug.cgi?id=1139056) that means bookmarks don't work correctly).
For most repos, I use `upstream` to point to the read-only copy of the repository of record:
For Gecko, the firefoxtree extension defines `central`, `incoming`, `aurora`, and so on.

Note that I had to check a box in the Bitbucket repository settings to make the repository non-publishing.

You'll also need a review repository (except for Gecko, where firefoxtree defines it for you):

    review = ssh://reviewboard-hg.mozilla.org/build-mozharness

## Hacking

When I start working on a new task, I first need to get a clean copy of the code.
That requires 

    hg pull upstream
    hg up -C default

Then I create a new bookmark for the project I'm working on, generally named after the bug ID

    hg bookmark bug1122334

I then hack and commit, trying to generate small, meaningful commits (microcommits).

When I've added a little bit extra to the most recent commit, I can update that commit with `hg commit --amend`.
When I've made a few changes that I want to commit separately, `hg record` is the tool for the job, similar to `git add -p`.

In my Git workflow, I generally break my commits along conceptual boundaries, but as I write I find myself wanting to add this or that bit of code to an already-committed unit.
In Git, I use `git commit --fixup <sha1>`.
Mercurial doesn't have quite that level of convenience, but I can commit with a helpful message like `hg commit -m "fixup preliminary stuff"`.

Once I have a few such commits, or otherwise want to directly manipulate the last few commits, I use `hg histedit`, passing it the earliest commit I wish to edit (different from Git!)

I'll periodically rebase this on top of the upstream code, to avoid bitrot:

    hg rebase -b bug1122334 -d default

I make sure my work is duplicated elsewhere by pushing periodically.
Since my Bitbucket repo is non-publishing, this doesn't change my commits to the immutable "public" phase.
The `-B` option updates the remote bookmark.

    hg push -r . -f -B bug112234

This operation is slow -- go-get-a-sandwich slow -- and I'm not sure if that's due to Mercurial or Bitbucket or both.

## Switching projects

To work on a different project, just run `hg up -C bug2233445`.

## Review

Once I have a set of commits I'm happy with, it's time for review.
First, see what changes will go out for review:

    hg outgoing -r . review

and if you're happy with it,

    hg push -r . review

You'll get a link to [https://reviewboard.mozilla.org](https://reviewboard.mozilla.org).
Follow that link, make sure everything is OK, pick reviewers for each commit, and then publish the review request.

## More

That's about as far as I've gotten so far.
The following links were helpful in getting set up, and have suggestions for further improvements:

 * [http://gregoryszorc.com/blog/2014/06/23/please-stop-using-mq/](http://gregoryszorc.com/blog/2014/06/23/please-stop-using-mq/)
 * [http://gregoryszorc.com/blog/2014/06/30/track-firefox-repositories-with-local-only-mercurial-tags/](http://gregoryszorc.com/blog/2014/06/30/track-firefox-repositories-with-local-only-mercurial-tags/)
 * [http://ahal.ca/blog/2015/new-mercurial-workflow/](http://ahal.ca/blog/2015/new-mercurial-workflow/)
 * [http://ahal.ca/blog/2015/new-mercurial-workflow-part-2/](http://ahal.ca/blog/2015/new-mercurial-workflow-part-2/)
