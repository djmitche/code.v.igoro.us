---
layout: post
title:  "SSH With Snow Leopard"
date:   2010-07-10 15:27:00
---


I
 just upgraded my Macbook to Snow Leopard, and the upgrade has changed
the way SSH authentication works.  I have set up a system I like quite a
 bit, now, and thought I would share. My usage pattern is that I do most
 of my work via [GNU screen](http://www.gnu.org/software/screen/) running on my login server, <tt>euclid</tt>.  So I want a simple procedure that will connect me to that screen session, with a proper SSH agent set up.

Snow Leopard automatically starts an <tt>ssh-agent</tt> process at login.  This is great, but does not interoperate with [SSHKeychain](http://sshkeychain.sourceforge.net/).
  Dropping SSHKeychain is OK with me - I don't use SSH tunnels, so it
really only acted as a GUI for passphrase entry.  It also ate CPU
occasionally, which of course causes the macbook to become more
painfully hot than usual.

So I
have three problems to solve: 1\. automatically add my key to ssh-agent;
2\. automatically expire the key at appropriate times (at my paranoia
level, that's at system sleep); and 3\. make multiple agent instances
usable from the same shell session on the server.

# Adding the Key at Connection Time

Adding the key is relatively straightforward.  I wrote a short script that Terminal runs when I hit ⌘-N or ⌘-T:

    #! /bin/bash

    # does ssh-agent not have a key?
    if ! ssh-add -l; then
        ssh-add ~/.ssh/dustin || exit 1
    fi

    exec ssh -x -t euclid.r.igoro.us bin/startscreen

This
will prompt me for the passphrase when there is not already a key
active, but proceed directly to the ssh invocation if the key situation
is OK.  The <tt>-x</tt> option to <tt>ssh</tt> is there to turn off X11
forwarding; without this option, SSH will helpfully start the X11 app.  I
 think this is a great feature, but I don't use X11 apps very often, so
I've disabled it.

# Expiring the Key Automatically

Mac
OS has a nicely designed system in place to allow applications to get
notified when the system is changing power states.  However, I wasn't
interested in writing a full OS X app for this particular project.
Enter [sleepwatcher](http://www.bernhard-baehr.de/).  This is
 a beautifully simple program that just executes scripts on particular
power events.  I set this up to run via launchd, as directed in the
README, and to run <tt>~/.ssh/sleep</tt> on sleep.  That script contains:

    #! /bin/bash

    # first, don't inherit a socket (sleepwatcher doesn't get the user's env)
    SSH_AUTH_SOCK=

    # find some sockets
    echo ".ssh/sleep:" `id`
    for sock in /tmp/launch-*/Listeners; do
        if [ -w $sock ]; then
            echo "Trying to remove .ssh/dustin from socket $sock"
            SSH_AUTH_SOCK=$sock /opt/local/bin/ssh-add -d ~/.ssh/dustin
        else
            echo "Skipping unwritable socket $sock"
        fi
    done

The for loop is required because a script run from sleepwatcher doesn't inherit the <tt>SSH_AUTH_SOCK</tt>
 variable that points to the running SSH agent.  The loop simply
searches for a writable SSH socket of the pattern used by the system's
agent.

# SSH Agent and Screen

If
you naïvely set up an SSH agent, connect to a remote system, and start
screen there, things will work great - until you disconnect from the
screen session.  When you connect to the remote system, SSH forwards the
 agent connection for you, and sets <tt>SSH_AUTH_SOCK</tt> on the remote
 system to point to this forwarded socket.  Screen passes this variable
along blindly, so it appears in all of the shells opened in screen
windows, and things work as you'd expect.  When that SSH connection is
removed, and a new one established, the forwarded agent appears at a new
 socket.  But those shells running in screen windows are still pointing
to the old name, and will no longer be able to connect.

The
fix is to create a socket with a well-known name that will not change
from connection to connection.  The following script takes care of it.
WARNING: this script is vulnerable to /tmp race conditions.  I am the
only user on my servers, so this doesn't bother me, but fixing it should
 be relatively straightforward.

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

