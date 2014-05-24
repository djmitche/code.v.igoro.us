---
layout: post
title:  "Solving an Encoding Mystery"
date:   2010-03-15 11:52:00
---


I don't write about it here, but I've been getting into brewing beer.  I downloaded an app for my iPhone, [iBrewMaster](http://www.ibrewmaster.com/iBrewMaster/Welcome.html), which helps me store recipes and track batches of homebrew through the brewing, fermeting, and serving stages.

I recently decided to make a clone of Dogfish Head's [Raison D'être](http://www.dogfish.com/brews-spirits/the-brews/year-round-brews/raison-detre.htm).
  This beer is fantastic, but that's beside the point.  I added the
recipe to the app, and clicked save.  In the menu, however, I saw
"Raison D'√™tre".  Not pretty.  The app has a feature where you create a
 "batch" from a particular recipe.  I did so, and the name of the batch
appeared as "Raison D'‚àö‚Ñ¢tre".  Even worse!
 I emailed the app developer, who replied almost immediately regarding
how he was handling encodings.  I won't go into detail, except to say
that he is careful to always encode strings before inserting them into
the internal SQLite database.

I
wanted to give him more information than a simple "well, it doesn't work
 and you should fix it!"  So I set about trying to replicate this
particular sequence of characters.  I know that Macs (and the iPhone is a
 Mac) have good support for encodings, so I assume the UI is not at
fault.  I know that the strings go into SQLite in UTF-8, and that SQLite
 just treats them as bytestrings, so a later SELECT will return the same
 UTF-8 bytestring as was specified in the INSERT.  So the error must
occurr somewhere between the SELECT and displaying the string on-screen.

## Character Encodings

A
word about encodings, with a bit of revisionist history.  In the
beginning, there was the Unicode Character Set.  Every funny squiggle
that the monks knew how to make on paper had a number - its Unicode
codepoint.  There are a _lot_ of Unicode characters - [95156](http://www.i18nguy.com/unicode/char-count.html) at last count.

Then
computers were invented, and we needed to represent, or encode, these
squiggles in only 7 bits each.  Someone (who probably only spoke
English) decided "well, you can only use the first 127 characters," and
thus ASCII was born.  If you want to write an "ñ" in ASCII, you'll have
to make do with "n".  Don't even ask about "葉".  We soon got a bit less
stingy (get it?), and with 8 bits available, everyone rushed to put
their favorite characters at code points 128-255 - regardless of what
Unicode put there.  For example, in latin-1, "ñ" is at code point 240\.
On a Mac, it's 150\.  Trying to decode a byte in the range 128-255 was a
challenge, because the encoding was usually unknown.  Those were dark
days, as chaos reigned.

Finally, some enlightened souls (Rob Pike and Ken Thompson) scratched out a new encoding [on a placemat](http://www.cl.cam.ac.uk/%7Emgk25/ucs/utf-8-history.txt).
  In this encoding, called UTF-8, all of the 7-bit ASCII characters
still fit in one byte, and look exactly the same.  But all of the other
characters take more than one byte, with some cleverness applied to make
 the encoding both compact and easy to decode reliably.  As a side note,
 the Unicode characters 128-255 match the latin-1 character set.

Now, if you have a sequence of unicode characters, say "青蛙吃我的餃子" that you want to store digitally, then you need to _encode_
 them, preferably in UTF-8, with the result being a bytestring.  When
you want the unicode characters back (perhaps to do some hyphenation),
you perform the reverse operation, and _decode_ from UTF-8 to Unicode Characters.

## Back to the Chase

A common mistake with multi-byte encodings is to assume that each byte is a distinct character, perhaps with a <tt>for</tt>
 loop indexing an array of bytes.  Since one character ("ê") turned into
 two ("√™"), this was a reasonable guess.  A little Python (in my
Unicode-enabled terminal) shows me the encoded form of "ê":

    >>> print `u"ê"`
    u'\xc3\xaa'

Treating those as Unicode characters instead of bytes is simple:

    >>> print u"Raison D'\u00c3\u00aatre"
    Raison D'Ãªtre

No
dice.  Another common mistake is to encode with one encoding, and decode
 with another.  This is especially common when the programming
environment "automatically" performs encodings or decodings.  For
example, Python has an annoying habit of decoding to ASCII, which
produces the infamous <tt>UnicodeEncodeError</tt>.

So let's try this out, guessing at the encoding that's used on the way out.

    >>> orig = u"Raison D'être"
    >>> print orig.encode('utf-8').decode('latin-1')
    Raison D'Ãªtre

The
result is the same as the single-byte treatment above.  Why?  Recall
that the latin-1 encoding is identical to Unicode in the range 128-255,
so treating a byte as a Unicode character is the same as treating it as a
 latin-1 character.

At this point, I perused the list of encodings Python supports, and "mac-roman" jumped out as a potential culprit.

    >>> print orig.encode('utf-8').decode('mac-roman')
    Raison D'√™tre

A match!  What about the longer string of nonsense in the batch name?

    >>> once = orig.encode('utf-8').decode('mac-roman')
    >>> print once.encode('utf-8').decode('mac-roman')
    Raison D'‚àö‚Ñ¢tre

Another match.

I
don't know much about iPhone internals, but I assume that the string
library treats a bytestring without any attached encoding as being in
the Mac-Roman character set.  When the value was selected out of the
recipes table, this decoding was done implicitly, followed by an
explicit UTF-8 encoding when inserting into the batches table, and
another implicit Mac-Roman decoding when selecting the batch for
display.

