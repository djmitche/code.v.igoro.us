---
layout: post
title:  "Charlieplexing: watch your voltage levels"
date:   2010-01-30 21:58:00
---


[Charlieplexing](http://en.wikipedia.org/wiki/Charlieplexing) is a technique to allow _n_ tristate digital output pins to control _n(n-1)_ LEDs, by exploiting the high-impedence state of the output pins and the reverse-bias tolerance of LEDs.

I put together a circuit to test this out, similar to the 6-LED diagram in the [Wikipedia entry](http://en.wikipedia.org/wiki/Charlieplexing#Expanding:_tri-state_logic).  I added three 220Ω resistors, though.  This ASCII art sums it up nicely:

         +--->|---+          +--->|---+          +--->|---+
         |  LED1  |          |  LED3  |          |  LED5  |
    <----|        |-/\/\-+---|        |-/\/\-+---|        |-/\/\-+-->
         |  LED2  |      |   |  LED4  |      |   |  LED6  |      |
         +---|<---+      R   b---|<---+      G   +---|<---+      B

where R, G, and B are the three connections to the Arduino, and the arrows on
the left and right side are joined by a jumper.  I put together some simple
Arduino-level code to drive this layout in a simple counter sequence, and fired
it up.

One thing I will say about the Arduino:
[tinkering](http://diveintomark.org/archives/2010/01/29/tinkerers-sunset) pays
off.  After the usual forgotten-semicolon cleanup, LEDs started blinking
immediately.  This is good, because I don't have much of an Arduino-debugging
toolbox at this point!

Anyway, there's a problem.  When an LED is fully illuminated, two other LEDs
glow at about 50% brightness.  For example, when LED1 is on, LED4 and LED6 glow
too.  It's not hard to see why: to turn LED1 on, the arduino drives R low and B
high.  The path through LED1 is intended, but LED4 and LED6 are also
forward-biased in series, albeit with more resistance inline and the
voltage-drop from two LEDs.  Can this be prevented?

Let's work out the math here, using the resistance _r_ as the only parameter I
can change.  The LEDs I'm using ([5mm Green LEDs from CHINA YOUNG
SUN](http://www.sparkfun.com/commerce/product_info.php?products_id=9592)) don't
have a lot of performance data, but do list a forward voltage drop of 1.8-2.2V,
so let's use 2V.  My Arduino is running from the USB power at 5V.  The resistor
to the left of R defines the current through that leg for the remaining _5-2 =
3V_, so _I<sub>1</sub>_ is _3/r_.  On the leg containing LED4 and LED6 a total
of 1V remains across two resistors, so _I<sub>4</sub>_ and _I<sub>6</sub>_ are
both _1/2r_.

The LED datasheet lists a maximum average current (20ma) and peak current
(30ma), but doesn't list a minimum current.  Guessing 1ma, I need _1/2r <
0.001_, so _r > 500_.  At that point, though, _I<sub>1</sub>_ is just 6ma - not
nearly bright enough to impress, particularly with a 16% duty cycle when
multiplexing all 6 LEDs.  All the same, I figured I'd try it.  The closest
resistor I had was 470Ω, so I gave that a shot.  The result was bad on all
fronts: the expected LED is dim, and the unwanted LEDs are still visible.

I suspect that, to get this to work, I'd need to reduce the supply voltage to
something less than twice the LEDs' forward voltage drop.  Then two LEDs in
series would carry no current.  I considered doing this with a simple voltage
divider on each microcontroller pin, but this of course ruins the tri-state
behavior that's critical to charlieplexing.  I could build that by using two
transistors for each pin, but by that point the benefits of charlieplexing in
terms of component count are long lost.

So, in short, for good charlieplexing, make sure that your source voltage is
less than twice the _V<sub>f</sub>_ of your LEDs.

_[EDIT: it turns out, after some futzing that this also "works fine" if you
just leave out the ballast resistors.  Presumably this relies on a limited duty
cycle and a "high enough" internal resistance to not melt the LEDs]_

