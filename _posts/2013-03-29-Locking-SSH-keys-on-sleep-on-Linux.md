---
layout: post
title:  "Locking SSH keys on sleep on Linux"
date:   2013-03-29 12:42:00
---


I
 got a new laptop, a ThinkPad X1 Carbon, and I'm running Linux on it.
So you're in for a series of posts describing the complex process I had
to follow to accomplish simple things.  Spoiler alert: 2013 is not the
year of Linux on the desktop.  It's not looking good for 2014 either.

I'm
running Fedora 18\.  I tried Ubuntu 12.10, but Unity couldn't hold itself
 together long enough to actually do anything, so I started over with
Fedora.

## SSH Agent

Gnome runs a nice keychain app that acts like (but is not) OpenSSH's ssh-agent.  The one obvious place it differs is that `ssh-add -l` will list keys even if they are "locked" (passphrase not supplied).

As long as you point the SSH_AUTH_SOCK variable to the right place, the agent works just fine for unlocking keys - it finds any private/public pairs in `~/.ssh`, and prompts to unlock them once you issue an SSH command that needs a key.  The problem is, it never re-locks the keys.

## Locking

Personally,
 I use SSH constantly while my laptop is awake, so I don't want an
arbitrary timeout.  Instead, I'm careful to put it to sleep when I'm
away from the keyboard.  So I want a way to lock the key on sleep.

It
turns out that pm-utils will run scripts in /etc/pm/sleep.d on sleep and
 wake.  It runs them as root, unfortunately.  I added the following in `01dustin-ssh-agent.sh`:

    #!/bin/sh

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

and then added the following in `~/bin/ssh-lock`:

    #!/bin/sh

    # drop keys from the SSH agent, using the same trick as bin/startscreen to find
    # that agent

    base="/tmp"
    [ -d /run/user ] && base="/run/user/$(id -u)"
    socket_dir="$base/$(uname -n)-$(id -u)"
    SSH_AUTH_SOCK=$socket_dir/agent ssh-add -D

See [my post](http://code.v.igoro.us/archives/60-SSH-With-Snow-Leopard.html)
 on tunneling ssh-agent into a screen session for the reference to
bin/startscreen.  I'm not sure how best to accomplish this without such a
 trick.  I'll work on that and post again.

