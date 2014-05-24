---
layout: post
title:  "virtualenv for Perl"
date:   2010-11-11 11:48:00
---


I absolutely love [virtualenv](http://pypi.python.org/pypi/virtualenv) for Python development.  It allows me to develop [Buildbot](http://buildbot.net/)
 against several versions of Python and several versions of its
dependencies, without modifying my system's Python installation at all!

Now, I need to do the same thing in Perl.  So I thought I'd compare the two side-by-side.

## virtualenv

    # install virtualenv locally
    wget http://bitbucket.org/ianb/virtualenv/raw/tip/virtualenv.py
    # set up a sandbox
    python virtualenv.py sandbox
    # activate it
    source sandbox/bin/activate
    # start installing stuff
    easy_install buildbot

## local::lib

There is no local::lib gentoo ebuild!  I'm sure there's a good reason, but that's odd all the same!

    # install local::lib locally
    wget http://search.cpan.org/CPAN/authors/id/G/GE/GETTY/local-lib-1.006007.tar.gz
    tar -zxf local-lib-1.006007.tar.gz
    cd local-lib-1.006007
    perl Makefile.PL --bootstrap # (accept lots of defaults)
    make test && make install
    # activate it (permanently)
    echo 'eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)' >>~/.bashrc
    eval $(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)
    # start installing stuff
    perl -MCPAN -e install Config::General # (I have to accept the same defaults again??)

I think virtualenv is the clear winner here!

