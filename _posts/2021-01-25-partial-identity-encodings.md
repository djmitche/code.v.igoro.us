---
title: The Horrors of Partial-Identity Encodings -- or  -- URL Encoding Is Hard
layout: post
date: 2021-01-25 00:00:00
categories: [mozilla]
---

URL encoding is a pretty simple thing, and has been around forever.
Yet, it is associated with a significant fraction of bugs in web frameworks, libraries, and applications.
Why is that?
Is there a larger lesson here?

# URL Encoding

If you've been lucky enough not to cross paths with HTTP in the last 30 years, then perhaps a refresher on URL encoding is in order.
URL encodings are behind the prevalence of `%` in long URLs, such as `https://example.com/download/test%2Flogs%2Fdebug.log`.

The encoding is a way of embedding arbitrary ASCII strings in a URI.
"Reserved" characters, `!#$&'()*+,/:;=?@[]`, are replaced by `%xx` where `xx` is the hex representation of the ASCII code for the character.
So `/` is replaced with `%2F` or `%2f`, `:` by `%3A` or `%3a`, and so on.
The `%` character itself maps to `%25`.

There are some issues with this encoding.

Precisely when a character must be escaped depends on the context.
For example, if used in the _path_ portion of a URI, `/` has special meaning and must be escaped as in the example above, while `=` has no special meaning.
But in the _query_ portion of a URI, the opposite is true: `=` separates keys from values, while `/` has no special meaning.

# Partial-Identity

I totally made up this term, but here's why it makes sense.
An identity encoding (for example, [in the Content-Encoding header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding#directives)) is an encoding that makes no changes -- input equals output.
URL encoding acts like an identity encoding for some inputs -- `marble magic` encodes to `marble magic`.
But for other inputs, it is not -- `omg! snakes!` encodes to `omg%21 snakes%21`.
Hence, "partial identity".

I assert that such encodings cause bugs and should be avoided in systems design.

# Bugs

A bit of searching, or for many of us a moment's recollection, will uncover a wealth of URL-encoding-related bugs.

The simplest class of bugs occurs when two communicating systems don't agree about when or what to encode or decode.
This can occur when a client generates a URL naively, such as `url = base_url + '/' + filename`.
