from dateutil.parser import parse
from bs4 import BeautifulSoup

class hCalendar(object):
    def __init__(self, markup):
        self._soup = BeautifulSoup(markup)
        self._cals = self._soup.findAll(attrs='vcalendar')
        if self._cals:
            self._cals = map(vCalendar, self._cals)
        else:
            self._cals = [vCalendar(self._soup)]

    def __len__(self):
        return len(self._cals)

    def __iter__(self):
        return iter(self._cals)

    def __getitem__(self, key):
        return self._cals[key]

    def getCalendar(self):
        return self._cals

class vCalendar(object):
    def __init__(self, soup):
        self._soup = soup
        self._events = map(vEvent, self._soup.findAll(attrs='vevent'))

    def __str__(self):
        return str(self._soup)

    def __len__(self):
        return len(self._events)

    def __iter__(self):
        return iter(self._events)

    def __getitem__(self, key):
        return self._events[key]

    def getEvents(self):
        return self._events

class vEvent(object):
    ATTR_DATETIME = ('dtstart', 'dtend', 'dtstamp', 'last_modified')
    ATTR_CONTENT  = ('summary', 'description', 'location', 'category', 'status', 'duration', 'method', 'uid', 'url')

    def __init__(self, soup):
        self._soup = soup
        self._content = {}
        self._datetime = {}
        
    def __str__(self):
        return str(self._soup)
        
    def __dir__(self):
        return list(self.ATTR_CONTENT + self.ATTR_DATETIME)
        
    def __getattr__(self, attr):
        if attr in self.ATTR_DATETIME:
            return self.getDatetime(attr.replace('_', '-'))
        elif attr in self.ATTR_CONTENT:
            return self.getContent(attr)
        raise AttributeError

    def getDatetime(self, attr):
        if not attr in self._datetime:
            content = self.getContent(attr)
            if content:
                self._datetime[attr] = parse(content)
            else:
                self._datetime[attr] = None
        return self._datetime[attr]

    def getContent(self, attr):
        if not attr in self._content:
            soup = self._soup.find(attrs=attr)
            if not soup:
                return None
            subs = soup.findAll(attrs='value')
            soup = subs if subs else [soup]
            content = ''
            for elem in soup:
                if elem.name == 'abbr':
                    content += elem['title']
                elif elem.name == 'time':
                    content += elem['datetime']
                elif elem.name in ['img', 'area']:
                    content += elem['alt']
                else:
                    content += self._getContent(elem)
            self._content[attr] = content
        return self._content[attr]

    def _getContent(self, soup):
        if soup.string:
            return soup.string.strip().strip('"')
        contents = []
        for elem in soup.contents:
            contents.append(self._getContent(elem))
        if not contents:
            return ''
        return max(contents, key=len)
