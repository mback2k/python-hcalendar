#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from hcalendar import hCalendar

try:
    import urllib.request as urllib2
except:
    import urllib2

def parsePage(url):
    print('-'*79)
    print(url)
    file = urllib2.urlopen(urllib2.Request(url, headers={'User-agent': 'WebGCal'}))
    hcal = hCalendar(file)
    for cal in hcal:
        for event in cal:
            print('-'*79)
            for attr in dir(event):
                print('%s: %s' % (attr, repr(getattr(event, attr))))

parsePage('http://web.archive.org/web/20140213063519/http://ufxtract.com/testsuite/hcalendar/hcalendar1.htm')
parsePage('http://web.archive.org/web/20130602094644/http://ufxtract.com/testsuite/hcalendar/hcalendar2.htm')
parsePage('http://web.archive.org/web/20110830165439/http://ufxtract.com/testsuite/hcalendar/hcalendar3.htm')

parsePage('http://web.archive.org/web/20110827224530/http://ufxtract.com/testsuite/hcalendar/hcalendar4.htm')
parsePage('http://web.archive.org/web/20110828213628/http://ufxtract.com/testsuite/hcalendar/hcalendar5.htm')

parsePage('http://web.archive.org/web/20110827233032/http://ufxtract.com/testsuite/hcalendar/hcalendar6.htm')
parsePage('http://web.archive.org/web/20110828213623/http://ufxtract.com/testsuite/hcalendar/hcalendar7.htm')

parsePage('http://web.archive.org/web/20110831030559/http://ufxtract.com/testsuite/hcalendar/hcalendar8.htm')
parsePage('http://web.archive.org/web/20110802163338/http://ufxtract.com/testsuite/hcalendar/hcalendar9.htm')

parsePage('http://web.archive.org/web/20110804082640/http://ufxtract.com/testsuite/hcalendar/hcalendar10.htm')
parsePage('http://web.archive.org/web/20110831025245/http://ufxtract.com/testsuite/hcalendar/hcalendar11.htm')

parsePage('http://web.archive.org/web/20110831052906/http://ufxtract.com/testsuite/hcalendar/hcalendar12.htm')
parsePage('http://web.archive.org/web/20110830165503/http://ufxtract.com/testsuite/hcalendar/hcalendar13.htm')

parsePage('http://web.archive.org/web/20130530044503/http://ufxtract.com/testsuite/hcalendar/hcalendar14.htm')

parsePage('http://microformats.org/wiki/hcalendar')

parsePage('http://en.wikipedia.org/wiki/List_of_House_episodes')
parsePage('http://en.wikipedia.org/wiki/List_of_NCIS_episodes')
parsePage('http://en.wikipedia.org/wiki/List_of_Fringe_episodes')
parsePage('http://en.wikipedia.org/wiki/List_of_Scrubs_episodes')
