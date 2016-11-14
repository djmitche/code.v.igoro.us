---
layout: post
title:  "Remote GPG Agent"
date:   2015-11-27 12:00:00
categories: [mozilla]
---

Private keys should be held close -- the fewer copies of them, and the fewer people have access to them, the better.
SSH agents, with agent forwarding, do a pretty good job of this.
For quite a long time, I've had my SSH private key stored only on my laptop and desktop, with a [short script to forward that agent into my remote screen sessions](http://code.v.igoro.us/posts/2014/05/Threading-an-SSH-Agent-Through-Screen.html).
This works great: while I'm connected and my key is loaded, I can connect to hosts and push to repositories with no further interaction.
But once I disconnect, the screen sessions can no longer access the key.

Doing the same for GPG keys turns out to be a bit harder, not helped by the lack of documentation from GnuPG itself.
In fact, as far as I can tell, it was impossible before GnuPG 2.1, and a great deal more difficult before OpenSSH 6.7.

I don't want exactly the same thing, anyway: I only need access to my GPG private keys once every few days (to sign a commit, for example)
So I'd like to control exactly when I make the agent available.

The solution I have found involves this shell script, named `remote-gpg`:

    #! /bin/bash

    set -e

    host=$1
    if [ -z "$host" ]; then
        echo "Supply a hostname"
        exit 1
    fi

    # remove any existing agent socket (in theory `StreamLocalBindUnlink yes` does this,
    # but in practice, not so much - https://bugzilla.mindrot.org/show_bug.cgi?id=2601)
    ssh $host rm -f ~/.gnupg/S.gpg-agent
    ssh -t -R ~/.gnupg/S.gpg-agent:.gnupg/S.gpg-agent-extra $host \
        sh -c 'echo; echo "Perform remote GPG operations and hit enter"; \
            read; \
            rm -f ~/.gnupg/S.gpg-agent'; 


The critical bit of configuration was to add the following to `.gnupg/gpg-agent.conf` on my laptop and desktop:

    extra-socket /home/dustin/.gnupg/S.gpg-agent-extra

and then kill the agent to reload the config:

    gpg-connect-agent reloadagent /bye

The idea is this: the local GPG agent (on the laptop or desktop) publishes this "extra" socket specifically for forwarding to remote machines.
The set of commands accepted over the socket is limited, although it does include access to the key material.
The SSH command then forwards the socket (this functionality was added in OpenSSH 6.7) to the remote host, after first deleting any existing socket.
That command displays a prompt, waits for the user to signal completion of the operation, then cleans up.

To use this, I just open a new terminal or local screen window and run `remote-gpg euclid`.
If my key is not already loaded, I'm prompted to enter the passphrase.
GPG even annotates the prompt to indicate that it's from a remote connection.
Once I've finished with the private keys, I go back to the window and hit enter.
