---
layout: post
title:  "Amanda's Transfer Mechanisms"
date:   2011-01-22 15:47:00
---


There's
 been a bit of confusion on the mailing list and IRC about how Amanda
assembles transfers out of transfer elements, and how transfer
mechanisms influence that.

In the final form of a transfer, any two adjacent elements must have
the _same_ mechanism.  For example is, an upstream element speaking
`XFER_MECH_PUSH_BUFFER` cannot talk to a downstream element using
`XFER_MECH_READ_FD` (nor, more confusingly, `XFER_MECH_PULL_BUFFER`).  So each mechanism is an
isolated definition of "here's how upstream and downstream should
talk".  They come in pairs because generally anything upstream can do
to downstream (e.g., upstream can write to downstream's fd) can occur
in reverse (e.g., downstream can read from upstream's fd).

What
makes this confusing is that if you specify a set of elements which
can't talk directly to one another, then xfer.c will add "glue" elements
 _between_ the specified elements.  To make that concrete, imagine you specify a transfer as

    source-holding --> filter-xor --> dest-fd

(if you like practical examples, then imagine filter-xor is a
buffer-based decompression filter, and you're pulling data from holding
disk, decompressing, and sending to a pipe -- something amfetchdump
would do).  Here are the mechanisms supported by each element:

    source-holding:
    XFER_MECH_PULL_BUFFER

    filter-xor
    XFER_MECH_PULL_BUFFER (input) and
    XFER_MECH_PULL_BUFFER (output)
    or
    XFER_MECH_PUSH_BUFFER (input) and
    XFER_MECH_PUSH_BUFFER (output)

    dest-fd
    XFER_MECH_WRITEFD (input)

In
putting these together, source-holding and filter-xor can use the same
mechanism (`PULL_BUFFER`).  This leaves filter-xor using `PULL_BUFFER` for
output, but dest-fd does not support this.  So xfer.c adds a glue
element that can speak `PULL_BUFFER` on input and `WRITEFD` on output.  This
 element basically loops in a thread, calling `upstream->pull_buffer`
and `write(downstream->input_fd, buffer)`.  So the final xfer looks
like

    source-holding --(PULL_BUFFER)--> filter-xor --(PULL_BUFFER)--> glue --(WRITEFD)--> dest-fd

Hopefully that helps to explain how the glue works.

Note
that one of the cool things about this arrangement is that in most cases
 the complexity is in the glue, not the elements.  In fact, in this case
 the glue provides the only thread that's required to run this transfer,
 so the other three element implementations don't need to manage threads
 at all.

