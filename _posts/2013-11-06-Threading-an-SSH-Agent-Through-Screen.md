---
layout: post
title:  "Threading an SSH Agent Through Screen"
date:   2013-11-06 12:13:00
---


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

    #! /bin/bash
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
    [ -e $socket_file ] && rm $socket_file

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
    </div>
  </body>
</html>
