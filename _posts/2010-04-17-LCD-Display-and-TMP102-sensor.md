---
layout: post
title:  "LCD Display and TMP102 sensor"
date:   2010-04-17 22:22:00
---


It is _incredibly_
 easy to throw things together with an Arduino.  It's common to see
criticism of the device when it's used in in projects that don't require
 even a fraction of its power, and that might be justified.  As a
flexible platform for test-driving complex modules, though, the Arduino
hits the mark perfectly on flexibility and usability.

I
don't have a particular project in mind for my Arduino, but since I
don't have a multimeter or an oscilloscope, I want to use it as a test
harness for various basic components as I experiment with them.  To this
 end, I bought a cute [16x2 character amber LCD display](http://www.sparkfun.com/commerce/product_info.php?products_id=9054).  With thoughts of building a fermentation-temperature monitor and learning about the I<sup>2</sup>C bus, I also bought a relatively cheap [TMP102 and breakout board](http://www.sparkfun.com/commerce/product_info.php?products_id=9418).  With a little bit of reading, I was able to stitch them together quickly and easily.

## LCD Display

The
display I purchased is command-driven via a 4-bit parallel port.  It's a
 ST7066, compatible with HD44780\.  There are two datasheets available --
 one for the [ST7066](http://www.sparkfun.com/datasheets/LCD/st7066.pdf), and one for the [assembled board](http://www.sparkfun.com/datasheets/LCD/ADM1602K-NSA-FBS-3.3v.pdf).
  The latter adequately described the pinout through unattributed
copying from the former, but was otherwise useless.  "Qiu", "Chen", and
"Ye", all three of whom helpfully signed the cover page, should be
ashamed.  Anyway, here's a brief description of the pins and some more
details I culled from the ST7066 datasheet:

*   V<sub>ss</sub> (ground) and V<sub>dd</sub> (positive supply): these are rated up to 7V, so running from the Arduino's 5V supply is great.
*   V<sub>0</sub> sets the LCD contrast.  Short on jumpers, I initiallyassumed I could leave this unconnected to get "reasonable" contrast.Not so!  I tried setting up a few voltage dividers to get the rightcontrast, without any luck.  Plan to add a 10k pot between ground andthe positive supply, and tie the wiper to this pin.
*   RS (register select) selects whether an operation is to configuration registers (0) or RAM (1)
*   R/W (read/write) selects whether an operation reads or writes to the device
*   DB0-DB7 is the data bus
*   E (enable), strobed to move a byte across the data bus
*   LED+/LED- supply power to the LED backlight, and can be wired directly to the 5V supply.

The
Arduino has a lot of digital pins, but all the same it's handy to save a
 few pins.  The display supports reading character and font data, but
that's not much use: the Arduino can remember whatever it needs to.  So
we won't need the R/W pin, and can tie it to ground (read) instead.

The
display can operate in two data lengths (controlled by the DL
configuration bit).  In the default mode, only 4 bits (DB4-DB7) on the
parallel bus are used.  The display starts in 8-bit mode, but
fortunately the DL bit comes in at pin DB4, so it's relatively easy to
reset the data length with only 4 pins connected.  Note that there's an
odd sequencing required here, where you need to set 8-bit mode three
times _before_ setting 4-bit mode.  Don't worry, though: the Arduino _LiquidCrystal_ library takes care of that for you.

So
aside from pins tied to V+ or GND, we only need 6 digital I/O pins.
It's best to avoid the pins that have other functions on the Arduino: 0
and 1 are RS-232 I/O, and 13 is the onboard LED.  I used pins 2-5 for
the data bus, pin 12 for E, and pin 13 for RS, since that was at the top
 of the LiquidCrystal example.  V<sub>ss</sub>, LED-, and R/W go to GND; V<sub>dd</sub> and LED+ go to the 5V supply; and V<sub>0</sub> is wired as described above.

From there on out, it's a straightforward application of the _LiquidCrystal_ library:

    #include <LiquidCrystal.h>

    LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

    void setup() {
        lcd.begin(16, 2);
    }

    void loop() {
        lcd.setCursor(0, 0);
        lcd.print("Hello, World");
    }

Note
that the display itself is capable of a number of interesting things not
 supported by the library.  It has an 80-byte character memory, and can
scroll that through the display without rewriting the entire screen
every time.  It can also accept 8 custom 5x11 glyphs, making rudimentary
 animation possible.

## TMP102

The
TMP102 is ridiculously tiny - smaller than the SMD resistors that
Sparkfun has placed around it on the breakout board.  It senses
temperature internally, which means it's basically monitoring the
temperature of its leads.

The device speaks I<sup>2</sup>C (also known as the two-wire interface or SMBus), which makes it pretty easy to connect to the Arduino.  The MCU speaks I<sup>2</sup>C
 via hardware, so the corresponding Arduino library doesn't even need to
 bit-bang the data.  On the Duemilanove, it uses analog-in pin 4 for SDA
 and analog-in pin 5 for SCL.  You'll also need to hook up V+ to the **3.3V pin**
 on the Arduino (the device is only specified for 3.6V) and GND to the
TMP102's GND.  Finally, the TMP102's ADD0 pin can cleverly select one of
 four addresses for the device by tying it to one of these four pins.  I
 tied it to GND, giving address 0b1001000\.  ALARM is an output pin, so
you can leave it unconnected.

The
TMP102 is a very nice low-power device that's designed to handle several
 common tasks without any interaction from the MCU - it can trigger an
interrupt when the temperature strays from a configured boundaries, poll
 temperature on a relatively slow schedule, or even poll on command.  I
didn't use any of that, relying on the device to simply sample the
temperature on its own schedule.

The
TMP102 has four registers, but we'll only use one -- temperature (0b01).
  Like many devices, this one multiplexes addresses and data over the
same bus.  To read a register, you first select the register by writing
it to the device, then read the 16-bit value, again with the MSB first.
 Once a register is selected, it can be read multiple times.

The
device's temperature register contains a two's-complement 12-bit value,
left-aligned, where 0x7FF is 128°C; equivalently, a change of one unit
in the 12-bit value is equivalent to 0.0625°C.

## Putting it Together

The obvious combination of these tools is to display the ambient temperature on the LCD screen.  Here's the program to do so:

    #include <Wire.h>
    #include <LiquidCrystal.h>

    LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

    #define TEMP_REG 0b00000000
    int tmp102 = 0b1001000;  // with ADD0 tied to ground

    void setPR(int reg) {
        Wire.beginTransmission(tmp102);
        Wire.send(reg);
        Wire.endTransmission();
    }

    int getReg() {
        unsigned char lo, hi;

        Wire.requestFrom(tmp102, 2);
        hi = Wire.receive();
        lo = Wire.receive();
        return (hi << 8) + lo;
    }

    void setup()   {
        lcd.begin(16, 2);
        Wire.begin();
        setPR(TEMP_REG);
    }

    void show_temp() {
        int temp_reg = getReg();
        lcd.setCursor(0, 0);
        show_bin(temp_reg);

        temp_reg >>= 4;

        float temp_C = temp_reg * 0.0625;
        float temp_F = (temp_C * 9 / 5) + 32;

        lcd.setCursor(0, 0);
        lcd.print(temp_C);
        lcd.print("\xdf""C  ");
        lcd.setCursor(0, 1);
        lcd.print(temp_F);
        lcd.print("\xdf""F  ");
    }

    void loop() {
        show_temp();
    }

The <tt>setup</tt> function sets up the LCD, then uses <tt>setPR</tt> to point the TMP102 at the temperature register.  Subsequent reads will then return the 12-bit encoded temperature.  The <tt>loop</tt> function reads the temperature register, decodes it, and displays the result in both Celsius and Fahrenheit.

Note that this is horrendously inefficient: the TMP102 only measures temperature every 26ms or so, during which <tt>loop</tt>
 will probably run a half-dozen times, feeding the same time strings to
the LCD each run.  It would be much better to put the TMP102 in one-shot
 mode, and measure the temperature at a much lower frequency - say once a
 second - with a correspondingly low update frequency for the display.
I'll leave that as an exercise for the reader.

