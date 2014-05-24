import re
import sys

output = None

for line in sys.stdin:
    if line.startswith('</div></div><div style="clear: both;"></div><div class="entry">'):
        continue
    if line.startswith('<div xml:base="http://code.v.igoro.us/rss.php?version=2.0&amp;all=1" class="feedEntryContent">'):
        continue
    mo = re.search(r'^### .<span xml:base="[^"]*">([^<]*)</span>\]\(http://code.v.igoro.us/archives/([^)]*).html\)<div class="lastUpdated">([^<]*)</div>', line)
    if mo:
        title, slug, date = mo.groups()
        month, day, year, time, ampm = date.split()
        month = [None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(month)
        slug = re.sub(r'^\d+-', '', slug)
        day = int(day[:-1])
        year = int(year)
        hh, mm = map(int, time.split(':'))
        if ampm == 'PM' and hh < 12:
            hh += 12
        date = '%04d-%02d-%02d %02d:%02d:00' % (year, month, day, hh, mm)
        filename = '../_posts/%04d-%02d-%02d-%s.md' % (year, month, day, slug)
        title = title.replace('"', "'")
        output = open(filename, "w")
        print >>output, """\
---
layout: post
title:  "%s"
date:   %s
---
""" % (title, date)
        continue

    if output:
        line = line.replace(r'codevigorous_files/', '/img/')
        print >>output, line.rstrip()
