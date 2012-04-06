Basic hCalendar Parser
======================

Dependencies
------------
- isodate            [http://pypi.python.org/pypi/isodate/]
- Beautiful Soup 4   [http://www.crummy.com/software/BeautifulSoup/]

Installation
-------------
Install all dependencies by using the following commands:

    pip install isodate
    pip install BeautifulSoup4

Install the parser by cloning the source from github.com:

    git clone git://github.com/mback2k/python-hcalendar.git hcalendar

Basic Example
-------------
The hCalendar class accepts file-like objects and strings, basically anything supported by BeautifulSoup

    from hcalendar import hCalendar
    
    html = """<div class="vcalendar"><div class="vevent">
     <a class="url" href="http://conferences.oreillynet.com/pub/w/40/program.html">
      http://conferences.oreillynet.com/pub/w/40/program.html
     </a>
     <span class="summary">Web 2.0 Conference</span>:
     <abbr class="dtstart" title="2005-10-05">October 5</abbr>-
     <abbr class="dtend" title="2005-10-07">7</abbr>,
     at the <span class="location">Argent Hotel, San Francisco, CA</span>
    </div></div>"""
    
    hcal = hCalendar(html)
    for cal in hcal:
        for event in cal:
            print event.url
            print event.summary
            print event.dtstart
            print event.dtend
            print event.location

HTML source code taken from [microformats.org](http://microformats.org/wiki/hcalendar). Output will look like this:

    http://conferences.oreillynet.com/pub/w/40/program.html
    Web 2.0 Conference
    2005-10-05 00:00:00
    2005-10-07 00:00:00
    Argent Hotel, San Francisco, CA
