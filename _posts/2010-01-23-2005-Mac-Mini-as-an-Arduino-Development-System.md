---
layout: post
title:  "2005 Mac Mini as an Arduino Development System"
date:   2010-01-23 19:00:00
---


I
 have an early Mac Mini that's not good for much of anything anymore.
It's not too fast, and it's a 32-bit PPC chip, so most proprietary-blob
software is off-limits, meaning it doesn't make a good media PC.  I put
Gentoo on it, and decided to use it to interface with my new Arduino
Duemilanove.  I'm more interested in the Arduino as a processor I can
play with, rather than a gateway to flashing LEDs, so I don't want the
full IDE - just a compiler and assembler, and a USB-based programmer.

This post documents the process I followed to set all of this up.

## Smoketest

As a smoketest, I downloaded the Arduino application on my Macbook and
modified one of the blinkie examples to make a chaser for a 7-segment
display I had handy.  I tweaked the code, hooked up some jumpers, and
clicked the "Upload" button.  The code was pretty simple, but I did
encounter an elementary digital logic problem: my display was
common-anode, but a digital HIGH is +5V.  I can't simply ground the
common pin - what to do, then?  My confusion was based on the false
assumption that logic LOW is unconnected - of course, it's actually
ground.  So I connected the common anode to the +5V rail, and set up to
illuminate each segment with a LOW digital out signal (routed through a
220Ω resistor).  Here's the code:

## Software

Next up, installing the requisite software on the Mini.  First, the crossdev tools.  Most documentation suggests simply:

    emerge crossdev
    crossdev --target avr

But this failed:

    * ERROR: cross-avr/avr-libc-1.6.4 failed.
    * Call stack:
    *               ebuild.sh, line   49:  Called pkg_setup
    *   avr-libc-1.6.4.ebuild, line   40:  Called die
    * The specific snippet of code:
    *              die "AVR toolchain not found"
    *  The die message:
    *   AVR toolchain not found

The solution, available from [Gentoo bug #230343](http://bugs.gentoo.org/230343), is to add the <tt>--without-headers</tt> flag, which instructs the crossdev tool to build the compiler first, then the C library.  The <tt>-s4</tt> builds a stage-4 compiler, including the C++ frontend.

    crossdev -s4 --target avr --without-headers

This takes a _long_ time on a system of this vintage.

While I was in the root shell, I installed [avra](http://avra.sourceforge.net/), an AVR assembler:

    emerge avra

Next
up, the kernel driver.  For the particular board I have, I need kernel
support for the FTDI USB-to-serial chip.  The driver is <tt>ftdi_sio</tt>, and the kernel option is _Device Drivers -> USB Support -> USB Serial Converter Support -> USB FTDI Single Port Serial Driver_.  If you happen to be on a PPC machine, don't forget to run <tt>ybin -v</tt> after upgrading the kernel.  With this set up, the USB serial device appears at <tt>/dev/ttyUSB0</tt>.

Finally, the programmer.  I'm using [avrdude](http://www.nongnu.org/avrdude/).
  I installed this from portage.  I had to install version 5.8
(keyworded ~ppc) to get the ATMEGA328P support.  The problem is, avrdude
 doesn't automatically reset the device by pulsing DTR. The Arduino IDE
does this just before running avrdude.  There is a patch available on [Avrdude bug #6866](http://savannah.nongnu.org/patch/?6866),
 but it hasn't yet been merged.  Rather than try to set up an avrdude
ebuild in a local portage overlay, I opted for the simpler solution
described [in the arduino.cc forums](http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1201441300): reset the device with a perl script just before invoking avrdude.  The code is simple:

I needed to emerge dev-perl/Device-SerialPort first. Then, to upload a new program:

    ./pulse && avrdude -c arduino -b 57600 -p m328p -D -U flash:w:/tmp/Blink.cpp.hex:i -P /dev/ttyUSB0

## Compiling

Up to
 now, I've been using Blink.cpp.hex, compiled earlier on the Macbook.
Now it's time to start building locally.  All of the libraries and
headers that make an Arduino sketch into an executable are in the <tt>dev-embedded/arduino</tt> ebuild.  I keyworded this (~x86 since there's no ppc keyword in the ebuild) and added <tt>USE=-java</tt> since I don't need the IDE, and emerged it.

I copied <tt>/usr/share/arduino-0017/hardware/cores/arduino/Makefile</tt> into my sketch directory and ran make.  The result:

    /bin/sh: /usr/share/arduino-0017/hardware/cores/arduino/Print.d: Permission denied

There are some comments in the ebuild about this -- apparently the IDE builds the <tt>.d</tt> files when it is first run, using group id <tt>uucp</tt>.  The easiest fix was just to run make as root, once, to build these files.

The Makefile references <tt>wiring_serial.c</tt>,
 but this file is not present in the distribution.  I removed it from
the Makefile.  Presumably I'll be on my own to configure serial I/O?

I'm
starting to get the impression that using the IDE is the smart way to go
 here!  The next error is from the linker, unable to find its script:

    /usr/libexec/gcc/avr/ld: cannot open linker script file ldscripts/avr5.x: No such file or directory

This is [Gentoo bug #147155](http://bugs.gentoo.org/show_bug.cgi?id=147155), which at the moment is not fixed.  The workaround:

    ln -s /usr/lib/binutils/avr/2.20/ldscripts /usr/avr/lib/ldscripts

And finally, we have a build:

    dustin@erdos ~/tmp/Blink $ make
    # Here is the "preprocessing".
    # It creates a .cpp file based with the same name as the .pde file.
    # On top of the new .cpp file comes the WProgram.h header.
    # At the end there is a generic main() function attached.
    # Then the .cpp file will be compiled. Errors during compile will
    # refer to this new, automatically generated, file.
    # Not the original .pde file you actually edit...
    test -d applet || mkdir applet
    echo '#include "WProgram.h"' > applet/Blink.cpp
    cat Blink.pde >> applet/Blink.cpp
    cat /usr/share/arduino-0017/hardware/cores/arduino/main.cxx >> applet/Blink.cpp
    /usr/bin/avr-gcc -mmcu=atmega168 -I. -gstabs -DF_CPU=16000000 -I/usr/share/arduino-0017/hardware/cores/arduino -Os -Wall -Wstrict-prototypes -std=gnu99  -o applet/Blink.elf applet/Blink.cpp -L. applet/core.a -L/usr/avr/lib -lm
    cc1plus: warning: command line option "-Wstrict-prototypes" is valid for Ada/C/ObjC but not for C++
    cc1plus: warning: command line option "-std=gnu99" is valid for C/ObjC but not for C++
    /usr/bin/avr-objcopy -O ihex -R .eeprom applet/Blink.elf applet/Blink.hex

    text    data     bss     dec     hex filename
        0    1244       0    1244     4dc applet/Blink.hex

running <tt>make upload</tt> as root, right after pressing the reset button in the board, successfully uploads the program.  Blinkies!

## Cleanup

A few
 small changes will make a lot of this easier.  First, I want to make
sure that the USB device is writable by a non-root user, using udev.
First, I used the following command to get the udev identifying
information for the device.

    udevadm info --attribute-walk -n /dev/ttyUSB0

The
identifiers for the device are given from most-specific to
least-specific.  The device itself doesn't have much to identify it:

    looking at device '/class/tty/ttyUSB0':
        KERNEL=="ttyUSB0"
        SUBSYSTEM=="tty"
        DRIVER==""

but I need something to match on this device, so I used <tt>SUBSYSTEM=="tty"</tt>.  To avoid confusion with other tty devices, though, I needed something more specific.  Looking at the parent entry, I see

        ATTRS{interface}=="FT232R USB UART"

which looks like a good identifier for this component.  Aside from setting the ownership and permissions, I decided to add a <tt>/dev/avr</tt> symlink, too.  The completed rule is:

    SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001" GROUP="users", MODE="0666", SYMLINK+="avr"

The first three fields match the device using the numbers from <tt>lsusb</tt>, and the last three set the proper group-id, mode, and dev-tree symlink for the device.  I put this rule in <tt>/etc/udev/rules.d/10-user.rules</tt> and updated udev:

    udevadm trigger

sure enough, <tt>/dev/avr</tt> now exists.  I added this path as the <tt>PORT</tt> in the Makefile.

The
second problem is that the makefile is not smart enough to reset the
unit before uploading.  That's easily fixed, using a variant of the <tt>pulse</tt> script from above, by adding a perl invocation to the Makefile (don't forget the whitespace must be a tab character!):

Finally, I commented out the value of <tt>CDEBUG</tt> in the Makefile, as I don't see any real utility for debug symbols on a microcontroller.

## Summary

This
turned out to be a lot of work -- the Arudino developers have done a
good job of encapsulating a lot of complexity in a nice, easy-to-use
IDE.  But now I can use my usual editor and workflow to develop programs
 for the ATMEGA328P, and that means a lot to me!

