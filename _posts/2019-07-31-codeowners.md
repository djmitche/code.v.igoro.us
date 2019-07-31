---
title: CODEOWNERS syntax
layout: post
date:   2019-07-31 16:14:09
categories: [mozilla]
---

The [GitHub docs page for CODEOWNERS](https://help.github.com/en/articles/about-code-owners) is not very helpful in terms of how the file is interpreted.
I've done a little experimentation to figure out how it works, and here are the results.

## Rules

For each modified file in a PR, GitHub examines the codeowners file and selects the *last* matching entry.
It then combines the set of mentions for all files in the PR and assigns them as reviewers.

An entry can specify no reviewers by containing only a pattern and no mentions.

## Test

Consider this CODEOWNERS:

```
*            @org/reviewers
*.js         @org/js-reviewers
*.go         @org/go-reviewers
security/**  @org/sec-reviewers
generated/**
```

Then a change to:

* `README.md` would get review from `@org/reviewers`
* `src/foo.js` would get review from `@org/js-reviewers`
* `bar.go` would get review from `@org/go-reviewers`
* `security/crypto.go` would get review from `@org/sec-reviewers` (but not `@org/go-reviewers`!)
* `generated/reference.go` would get review from nobody

And thus a PR with, for example:
```
M src/foo.js
M security/crypto.go
M generated/reference.go
```

would get reviewed by `@org/js-reviewers` and `@org/sec-reviewers`.

If I wanted per-language reviews even under `security/`, then I'd use

```
security/**       @org/sec-reviewers
security/**/*.js  @org/sec-reviewers @org/js-reviewers
security/**/*.go  @org/sec-reviewers @org/go-reviewers
```
