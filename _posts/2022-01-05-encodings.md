---
title: "Deep Dive: Text Encodings"
layout: post
date:   2022-01-05 01:00:00
categories: []
---

What follows is based on a presentation I made for Datadog support engineers.
It covers the basics of text encodings and some troubleshooting and problem-solving advice.
It can probably be of use to anyone working on supporting or troubleshooting encoding-related bugs.
Consider this an update to my [encodings post from 12 years ago](http://code.v.igoro.us/posts/2010/03/Solving-an-Encoding-Mystery.html).

# Definitions

Let's start with some definitions.

* *Bytes:* the smallest unit of data we can address in a file, in memory, or a network packet.
  I'll write these as two-digit hexadecimal numbers in a monospace font, like `0a` or `FE`.
  Upper-case and lower-case mean the same thing in hexadecimal.

* *Characters*: the things we might call "letters", plus some.
  For example, H  e   l   o    د   ل   پ and   ا are all characters.
  There are several kinds of "non-letter" characters, as well.
  An important kind, *control characters,* aren't visible, but give some other kind of instruction.
  For example, TAB means something like "move to the next tab stop", and LF (also known as newline) means to go on to the next line.
  In some character sets, each character has been given an official name, such as "Latin Small Letter D" or "Latin Capital Letter O With Stroke", to make them easier to talk about.

* *Codepoints:* numbers assigned to characters.  For example, we might say that 100 corresponds to "Latin Small Letter A", 101 to "Latin Small Letter B" and so on.

* *Strings:* sequences of characters.  For example, "こんにちは世界" is "Hiragana Letter Ko", "Hiragana Letter N", and so on.

# Character Sets

A *Character Set* is a collection of characters and their codepoints.

The oldest character set is [ASCII](https://en.wikipedia.org/wiki/ASCII), invented in 1961.
It contains the English alphabet (upper and lower case), Arabic digits, some punctuation, and control characters -- 128 characters in total.
This character set was built when computers were mostly used in the US academic and business context, and like any technology it embodies that social context.

Once digital communication began with people outside the US, additional characters were required.
This led to the creation of several character sets collectively referred to as "extended ASCII".
Each assigns *different* characters to codepoints 128-255.
For example:

 * [MacRoman](https://en.wikipedia.org/wiki/Mac_OS_Roman) assigns codepoint 192 = ¿
 * [Latin-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1) assigns codepoint 192 = À
 * [cp1253](https://en.wikipedia.org/wiki/Windows-1253) (a.k.a. Greek - ANSI) assigns codepoint 192 = ΐ

This immediately led to issues when data was written in one character set and read in another.

In one of those rare cases where the first idea to come to an engineer's head actually works, some smart people decided to make one "universal" character set that had all necessary characters assigned to unique codepoints.
The result is *Unicode*.
Unicode has a _lot_ of characters, and several sites like [unicode-table.com](https://unicode-table.com/en/) have nicely-designed interfaces to let you browse the available characters.

Unicode codepoints are typically written with a `U+` prefix and using a hexadecimal notation for the codepoint.
For example, [U+16A0](https://unicode-table.com/en/16A0/) is "Runic Letter Fehu Feoh Fe F" (ᚠ)  and [U+1F4C8](https://unicode-table.com/en/1F4C8/) is "Chart with Upwards Trend Emoji" (📈)
Don't be confused by the use of hex notation -- these are _not_ bytes.
Unicode has room for about a million characters, although only about 10% of those are defined just yet.
More are added every year.

Critically for compatibility, the first 128 codepoints of Unicode are identical to ASCII.

Putting all of this together, the phrase दिल तो पागल है 
is, in codepoints, U+0926 U+093F U+0932 U+0020 U+0924 U+094B U+0020 U+092A U+093E U+0917 U+0932 U+0020 U+0939 U+0948.
Note that [U+0020](https://unicode-table.com/en/0020/) (in decimal: 32) represents the "space" character, just as it does in ASCII.

# Encodings

A character set allows us to represent a string as a sequence of numbers, but that's not quite enough to enable us to represent it as a sequence of bytes.
For that, we need to encode the string, using an encoding.
An *encoding* defines how codepoints are represented as a byte sequence.

The earliest encoding is so simple that it's easy to miss: ASCII only uses 127 different codepoints, so encoding each codepoint into one byte works just fine.
In fact, extended ASCII stops at codepoint 255 precisely so that all codepoints can be encoded in a byte.
So, "hello" is encoded as `68 65 6c 6c 6f`.

## UTF-8

Unicode has more than 256 characters, but the designers wanted it to be compatible with ASCII for the very-common ASCII characters.
This would mean that most textual languages interpreted by a computer, like HTML, that are limited to the ASCII character set, would continue to work unchanged when treated as a Unicode-encoded string.
The solution was *UTF-8*.
This encoding uses one byte for codepoints 0-127, just like ASCII.
For the remaining codepoints, a multi-byte encoding is used that sets the "high bit" of all bytes except the last.
For those who don't speak binary, that just means that the byte is greater than 128 (`80`).
So, for example:
 * [U+0926](https://unicode-table.com/en/0926/) - DEVANAGARI LETTER DA (द) → `e0 a4 a6`
 * [U+1F926](https://unicode-table.com/en/1F926/) - FACE PALM (🤦) → `f0 9f a4 a6`

The result is a sequence of bytes which, if it contains only ASCII characters, looks exactly like an ASCII text file from 1961.
Check out [another post of mine](http://code.v.igoro.us/posts/2021/01/partial-identity-encodings.html) for a preview of why that might prove problematic!

A disadvantage of UTF-8 is that, because a character may be represented by a variable number of bytes, it's difficult to "skip" a specific number of characters forward or backward in an encoded string.

UTF-8 is the dominant encoding in most areas.

## UTF-16

Most Unicode characters used in communication between living people are contained in what's called the [Basic Multilingual Plane](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane) (BMP).
This plane defines 2<sup>16</sup> codepoints, fitting nicely into two bytes (16 bits).
The UTF-16 encoding uses two bytes for each character in the BMP, with a mechanism to use four bytes for characters in other planes.
This has the advantage that most characters are exactly two bytes wide, partially alleviating the disadvantage noted above for UTF-8.
On the other hand, for most texts, the UTF-16 encoding is quite a bit longer than the UTF-8 encoding.

### Byte Order (Endianness)

There is also an issue of what order to write the two bytes.
For example, U+0926 - DEVANAGARI LETTER DA (द) can be encoded as `09 26` or `26 09`.
With modern technology, it seems like the standards authors could have just picked one of those options.
But at the time, CPUs had a preferred "endianness" and worked less efficiently with data in the opposite order.
A "little-endian" processor expects the least-significant byte to come first (`26 09`), while a "big-endian" processor expects the most-significant byte to come first (`09 26`).
Modern processors can be configured to use either endianness with no real difference in performance, but this relic remains.
The result is that there are actually two encodings:

 * UTF-16-LE: "banana" → `62 00 61 00 6e 00 61 00 6e 00 61 00`
 * UTF-16-BE: "banana" → `00 62 00 61 00 6e 00 61 00 6e 00 61`

In some cases, the only information about encoded data is that it is UTF-16, without an endianness specified.
When this is the case, the data typically begins with a "Byte Order Marker" (BOM), [U+FEFF](https://unicode-table.com/en/FEFF/).
In UTF-16-LE, this looks like `ff fe`, while in big-endian it looks like `fe ff`.
For example, `ff fe 62 00 61 00 6e 00 61 00 6e 00 61 00` is "banana" in UTF-16.

For a long time, Windows systems preferred UTF-16, and typically included the BOM.
Recently, Microsoft has been moving to prefer UTF-8.

## UTF-32

The natural evolution is to an encoding that uses four bytes for each codepoint, and that's precisely what UTF-32 is.
Four bytes can represent any Unicode codepoint, so UTF-32 is a fixed-length encoding, solving the skipping issues inherent to UTF-8 and UTF-16.
UTF-32 also has endianness, and can use the same BOM character to distinguish the two.

 * UTF-32-LE: "banana" → `62 00 00 00 61 00 00 00 6e 00 00 00 61 00 00 00 6e 00 00 00 61 00 00 00`

This encoding is quite large: nearly four times the size of UTF-8 for most strings.
As a result, it's rarely used for files on disk or in network communication.
It is, however, sometimes used internally by applications that must manipulate text; for example, Python uses it internally to support efficient string slicing.

## Shift-JIS

The great thing about standards is, there are just so many to choose from.
Unicode did not _quite_ vanquish its foes, and one particularly notable non-Unicode character-set and encoding is [Shift-JIS](https://en.wikipedia.org/wiki/Shift_JIS).

Shift-JIS defines a character set containing many symbols from ASCII, as well as a number of Japanese characters.
It is a variable-width encoding like UTF-8, but using a different encoding mechanism.
Like extended ASCII, it exists in an array of vendor-specific variants.

A critical characteristic is that the first 128 codepoints correspond to ASCII and are encoded with one byte, _except_ "\\" (Reverse Solidus) is replaced with "¥" (Yen Sign) and "~" (Tilde) is replaced with "‾" (Overline).
Seeing "¥" where you expect "\", such as `C:¥Program Files¥...`, is a good indication that you are dealing with Shift-JIS.

Shift-JIS is used on about 5% of Japanese-language websites,  or about 0.1% of the entire web.

# Problem Solving

Now that we understand the basics of encodings, let's look at how to troubleshoot encoding issues.
Let's start with a few general principles:

Always know if you are looking at bytes or characters, and use the appropriate tool for the two.
It never makes sense to encode bytes: an encoding converts a string into bytes.
Similarly, it never makes sense to decode a string: decoding converts bytes into a string.

In fact, always try to get back to the raw bytes.
If you are working with a user who has found a bug, try to get the bytes from them unchanged.
Compression tools like Zip and tar are good for this -- their job is to transport bytes intact, with no interpretation.
Clipboards are _not_ good for this: most modern systems store strings on their clipboard, encoding and decoding in the process.
And don't get me started complaining about the habit of sending screenshots of text files -- that definitely won't help!

Finally, know your tools.
Text editors, programming languages, and hex editors are all fantastic tools for investigating encoding problems, but they can also confuse the issue.
For example, some text editors will not display characters like [U+200B](https://unicode-table.com/en/200B/) Zero Width Space, or require enabling some "show hidden characters" option to see them.
Terminals and web browsers can also hide the truth.
Such tools are still useful, as long as you know their limitations.

## Hex Editors

The best way to see what's in a file is using a hex editor.
There are lots of these tools, but they all do about the same thing:

 * [`xxd`](https://linux.die.net/man/1/xxd)
 * [`hexdump -C`](https://linux.die.net/man/1/hexdump)
 * [Hex Fiend](https://hexfiend.com/)

All of them produce output that looks something like this:

```
dustin.mitchell@bell ~/tmp $ hexdump -C test.log
00000000  32 00 30 00 32 00 31 00  2d 00 31 00 30 00 2d 00  |2.0.2.1.-.1.0.-.|
00000010  31 00 32 00 20 00 30 00  39 00 3a 00 32 00 39 00  |1.2. .0.9.:.2.9.|
00000020  20 00 73 00 74 00 61 00  72 00 74 00 69 00 6e 00  | .s.t.a.r.t.i.n.|
00000030  67 00 20 00 75 00 70 00  0a 00 32 00 30 00 32 00  |g. .u.p...2.0.2.|
00000040  31 00 2d 00 31 00 30 00  2d 00 31 00 32 00 20 00  |1.-.1.0.-.1.2. .|
00000050  30 00 39 00 3a 00 33 00  30 00 20 00 45 00 52 00  |0.9.:.3.0. .E.R.|
00000060  52 00 4f 00 52 00 20 00  73 00 74 00 61 00 72 00  |R.O.R. .s.t.a.r.|
00000070  74 00 75 00 70 00 20 00  66 00 61 00 69 00 6c 00  |t.u.p. .f.a.i.l.|
00000080  65 00 64 00 20 00 3d d8  16 de 0a 00              |e.d. .=.....|
0000008c
```

Here the leftmost column is the number of bytes since the beginning of the file, followed by the bytes themselves.
The rightmost column gives the ASCII equivalent of each byte, with non-printable characters displayed with `.`.

Looking at this example, we can already make some conclusions based on the information above.
Based on the ASCII display on the right, the first few bytes appear to contain a date string ("2021-10-12"), and each character is two bytes long.
Looking at the hex values, every other byte of these ASCII characters is `00`, and the least-significant bytes of the codepoint are coming first.
So, this is probably UTF-16-LE.
At position 00000038, `0a 00` is [U+000A](https://unicode-table.com/en/000A) New Line, and we see a new log line begin after that newline.
What's going on at position 00000086?

## Python

A hex editor is great for seeing the data, but we'll need more powerful tools that implement all of the encodings, and know how to display non-ASCII characters.
My preference is for Python, although other scripting languages have similar functionalities -- use whatever you're familiar with.
Here's a quick cheat-sheet for some of Python's encoding-related functionality (noting that this is specific to Python 3):

The `open` built-in, when given the "rb" mode, will read bytes from a file:
```
>>> log = open("test.log", "rb").read()
>>> print(log.hex())
32003000320031002d00310030002d0…
```

If you have a short byte-sequence you want to type or paste, `bytes.fromhex` is the tool to use:
```
>>> status = bytes.fromhex('f0 9f a4 a6')
>>> print(status.hex())
f09fa4a6
```

Python represents bytes with `b'...'`, displaying ASCII printable characters directly and using escapes for everything else:
```
>>> log
b'2\x000\x002\x001\x00-\x001\x000\x00-\x001\x002\x00 …'
```

This representation is a bit hard to read.
The `.hex()` function will convert that to simple hex bytes, and it can even break those up with spaces

```
>>> print(log.hex())
32003000320031002d00310030002d003100…
>>> print(log.hex(' '))     # separator between bytes
32 00 30 00 32 00 31 00 2d 00 31 00 …
>>> print(log.hex(' ', 2))  # separator between pairs of bytes
3200 3000 3200 3100 2d00 3100 3000 …
```

You can decode bytes to a string with `decode`:

```
>>> log.decode('utf-16-le')
'2021-10-12 09:29 starting up\n2021-10-12 09:30 ERROR startup failed 😖\n'
```

The string representation displays control characters like `\n` explicitly.
To interpret those characters, use `print`:

```
>>> print(log.decode('utf-16-le'))
2021-10-12 09:29 starting up
2021-10-12 09:30 ERROR startup failed 😖    
```

Encoding is easy, too:

```
>>> '🐍'.encode('utf-8').hex(' ')
'f0 9f 90 8d'   # Snakes need a lot of bytes for their encoding
```

Note that you can't encode or decode the wrong thing:
```
>>> log.encode('utf-16-le')
AttributeError: 'bytes' object has no attribute 'encode'
>>> "🅰 🆂🆃🆁🅸🅽🅶".decode('utf-8')
AttributeError: 'str' object has no attribute 'decode'
```

## Incorrect Encodings

Most software engineering, globally, is done in English, so it's common for testing to occur only using English -- ASCII -- strings.
Just about every encoding is compatible with ASCII, so it's easy for engineers to miss encoding bugs.

Let's see what might go wrong if encoding and decoding aren't matched:

```
>>> print("Childlike".encode('utf-8').decode('latin-1'))
Childlike       # works for me!  –English-speaking software engineer
>>> print("Naïve".encode('utf-8').decode('latin-1'))
NaÃ¯ve          # hmm, that's not right..
>>> print("Naïve".encode('utf-8').decode('utf-16'))
慎꿃敶           # uhoh, mojibake!
```

## Mojibake

The output above is an example of [_mojibake_](https://en.wikipedia.org/wiki/Mojibake): the garbled text that results when encodings go awry.

To diagnose, go back as early as possible in the chain of handling of this data.  Get a file containing the data, ideally zipped.
Open it in a hex editor and apply your encoding expertise 🧠.

Often, mojibake contains [CJK characters](https://en.wikipedia.org/wiki/CJK_characters).
They are plentiful in the basic multilingual plane, so by chance they tend to appear often when bytes are incorrectly decoded with a Unicode encoding.
Be careful how you refer to this -- "mojibake" and "incorrectly decoded string" are good terms.
Words matter!

## Non-Printing Characters

Lots of characters have no visual representation, or a representation that's easy to miss.
For example:

 * [U+0000](https://unicode-table.com/en/0000) - Null
 * [U+0020](https://unicode-table.com/en/0020) - Space
 * [U+200A](https://unicode-table.com/en/200A) - Hair Space
 * [U+200B](https://unicode-table.com/en/200B) - Zero Width Space 😿
 * [U+202A](https://unicode-table.com/en/202A) - Left-To-Right Embedding

Many editors will hide these characters from you, leaving you puzzling as to what's wrong with the data.
This is where it's useful to know your tools, and to verify with a hex editor.

As an example of where this can go wrong, copying a filename out of the NTFS Security Properties dialog will include a [U+202A](https://unicode-table.com/en/202A) character on the clipboard.
Pasting that value into a configuration file may result in a config that _looks_ fine -- because the tool is hiding the character -- but fails to load because the file does not exist with that name.

Null is another insidious character.
Most terminals will do nothing with a Null, so things look fine even when they are not:

```
>>> print('Hello'.encode('utf-16-le').decode('utf-8'))
Hello
```

Python's string representation avoids this issue, showing that there is, indeed, a problem with that string:

```
>>> 'Hello'.encode('utf-16-le').decode('utf-8')
'H\x00e\x00l\x00l\x00o\x00'
```

## Replacement Characters

Most systems do not have fonts covering _every_ Unicode character, and will typically display a replacement character such as □ for unknown characters.
So output like "Hello, my name is □□□□□□" may actually be correct, and just not something that the font you are using can show.

A related character is [U+FFFD](https://unicode-table.com/en/FFFD/) Replacement Character (�).
This is used when an error occurs while decoding a string.
Python can do the same with `errors="replace"`:

```
>>> '🐍'.encode('utf-16-le').decode('utf-8', errors='replace')
'=�\r�'
```

If you see � in a string, go back to the bytes from which that string was decoded.
Likely those bytes were not in the expected encoding, or otherwise corrupted.

## Misalignment

One common form of corruption is, for multi-byte encodings, to get "misaligned".
UTF-8 is designed to be resistant to this issue, but UTF-16 is not.

For example, consider दिल तो पागल ह encoded in UTF-16-le:

```
26 09  3f 09  32 09  20 00  24 09  4b 09  20 00  2a 09  3e 09  17 09  32 09  20 00  39 09
```

and look at pairs of bytes after skipping one byte:
```
   09 3f  09 32  09 20  00 24  09 4b  09 20  00 2a  09 3e  09 17  09 32  09 20  00 39
```

The result is some truly collosal mojibake: "㼉㈉ ␀䬉 ⨀㸉ᜉ㈉ 㤀"

I was lucky enough to catch a misalignment issue from a copy-pasted string in a bug report.
On a guess, I tried adjusting the alignment, and got something that looked a lot like a log entry:

```
>>> mojibake='　㈀㄀ⴀ㄀㄀ⴀ㄀㤀 ㄀㄀㨀㈀㔀㨀㈀㌀⸀㈀㄀ 猀攀爀瘀攀爀㈀     䔀爀爀漀爀㨀 㔀　　　㄀Ⰰ 匀攀瘀攀爀椀琀礀㨀 ㄀㔀Ⰰ 匀琀愀琀攀㨀 ㄀'
>>> print(mojibake.encode('utf-16-le')[1:-1].decode('utf-16-le'))
021-11-19 11:25:23.21 server2     Error: 50001, Severity: 15, State:
```

# Conclusion

We've learned how some common character sets and encodings work, then looked at some tools and techniques for troubleshooting encoding issues.
Whether you're a support engineer debugging user issues or a software engineer hoping to get encodings "right" in new code, I hope this has been a helpful overview.
