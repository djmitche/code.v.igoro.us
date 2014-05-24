---
layout: post
title:  "irssi settings for status-in-nick"
date:   2010-10-22 13:06:00
---


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

    use strict;

    use vars qw ($VERSION %IRSSI);

    $VERSION = 'v1.0';
    %IRSSI = (
            name        => 'moznick',
            authors     => 'dustin',
            contact     => 'dustin@mozilla.com',
            url         => 'http://code.v.igoro.us/',
            license     => 'GPLv2',
            description => 'Sets my nick status for Mozilla co-workers',
            );

    use Irssi;

    my $last_nick = '';

    sub is_mozilla {
        my ($server) = @_;
        if (!$server || $server->{'chatnet'} eq 'mozilla') {
            return 1;
        }

        Irssi::print("This isn't a mozilla channel!");
        return 0;
    }

    sub cmd_moznick {
        my ($data, $server, $channel) = @_;

        if (is_mozilla($server)) {
            my $new_nick = $data? "dustin|$data" : "dustin";
            return if ($new_nick eq $last_nick);

            $server->command("NICK $new_nick");
            Irssi::print("nick set to $new_nick");
            $last_nick = $new_nick;
        }
    }

    Irssi::command_bind("moznick", "cmd_moznick");

This just adds a <tt>/MOZNICK</tt>
 command that will set my nick, but only on a Mozilla chatnet.  Then I
added an alias and some bindings.  I don't like irssi's
configuration-writing stuff, as it's several times blown away my
configuration.  Instead, I edit the config file directly.  So I have:

    aliases = {
        moznick_moz = "window goto #build; moznick $*";
    };

    keyboard = (
        { key = "meta-space"; id = "multi"; data = "command moznick_build"; },
        { key = "meta-z"; id = "multi"; data = "command moznick_build brb"; },
        { key = "meta-x"; id = "multi"; data = "command moznick_build away; command away"; }
    );

The advantage of the <tt>window goto</tt>
 in the alias is that it will switch to a channel on the mozilla
chatnet.  I'd love to have a way to just switch to that chatnet without
changing windows, but this isn't bad.

