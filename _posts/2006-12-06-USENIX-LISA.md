---
layout: post
title:  "USENIX LISA"
date:   2006-12-06 10:17:00
---


So what better time to inagurate this blog than now, during the
[keynote](http://www.usenix.org/events/lisa06/tech/#keynote) to the [LISA
(Large Installation Systems
Administration)](http://www.usenix.org/events/lisa06/index.html) conference.
It's an interesting general talk about one of the many pressing non-technical
issues in this community: DRM and restrictive licensing.

He's boiled it down nicely: in the traditional crypto challenge, Alice talking
to Bob, with Carol trying to eavesdrop, Carol has the ciphertext and the
cipher, but not the key -- that's the feature that differentiates Carol from
Bob, allowing Bob, but not Carol, to decrypt it.  But under DRM and other legal
challenges Carol and Bob are the same person.  Companies are sending cyphertext
to Carol/Bob, with the restriction that they can use it in one capacity (as
Bob, the consumer) but not in another (as Carol, the same consumer who wants to
watch the DVD on her computer).  Obviously, the only technical way to make this
work is to control the cipher (the algorithm).  It's easy to build a cipher to
do what they want.  It's technically impossible to prevent others from building
ciphers that don't.  So they turn to the law.

This all reminds me of the "good old days" of the Apple II and crazy technical
copy-protection schemes -- schemes which faded in popularity, and seem to have
come back in the last decade.  Doctrow's answer was, to put it simply, DMCA.
DMCA gave these companies the legal muscle they needed.

This keynote highlights what I'd like to talk about on this site -- I'm not
much interested in posting code samples, or kvetching about this language or
that language.  I'd rather talk about these much more important issues.

