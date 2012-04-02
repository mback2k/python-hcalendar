import re, bs4, isodate, datetime

class hCalendar(object):
    def __init__(self, markup):
        self._soup = bs4.BeautifulSoup(markup)
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

class vObject(object):
    REGEX_DATE = re.compile(r'P(\d{4})-(\d{2})-(\d{2})')
    REGEX_DATETIME = re.compile(r'P(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})')

    ATTR_RELATION = {}

    def __init__(self, soup):
        self._soup = soup
        self._content = {}
        self._datetime = {}
        self._duration = {}

    def __str__(self):
        return str(self._soup)

    def getDatetime(self, attr):
        if not attr in self._datetime:
            content = self.getContent(attr)
            if content:
                content = content.replace(' ', 'T')
                if not 'T' in content:
                    if ':' in content:
                        value = isodate.parse_time(content)
                    else:
                        value = isodate.parse_date(content)
                else:
                    value = isodate.parse_datetime(content)
                if isinstance(value, datetime.time):
                    self._datetime[attr] = datetime.datetime.min.replace(hour=value.hour, minute=value.minute, second=value.second, microsecond=value.microsecond, tzinfo=value.tzinfo)
                elif isinstance(value, datetime.date):
                    self._datetime[attr] = datetime.datetime(value.year, value.month, value.day)
                else:
                    self._datetime[attr] = value
            else:
                self._datetime[attr] = None
        return self._datetime[attr]

    def getDuration(self, attr):
        if not attr in self._duration:
            content = self.getContent(attr)
            if content and attr in self.ATTR_RELATION:
                if self.REGEX_DATETIME.match(content):
                    content = self.REGEX_DATETIME.sub(r'P\1Y\2M\3DT\4H\5M\6S', content)
                elif self.REGEX_DATE.match(content):
                    content = self.REGEX_DATE.sub(r'P\1Y\2M\3D', content)
                relation = getattr(self, self.ATTR_RELATION[attr])
                value = isodate.parse_duration(content)
                if isinstance(value, isodate.duration.Duration):
                    self._duration[attr] = value.tdelta + relation + datetime.timedelta(days=365*value.years) + datetime.timedelta(days=30*value.months)
                else:
                    self._duration[attr] = value + relation
            else:
                self._duration[attr] = None
        return self._duration[attr]

    def getContent(self, attr, sep=None, all=False):
        if not attr in self._content:
            soup = self._soup.find(attrs=attr)
            if not soup:
                return None
            self._content[attr] = self._getContent(soup, sep, all)
        return self._content[attr]

    def _getContent(self, soup=None, sep=None, all=False):
        if not soup:
            soup = self._soup
        subs = soup.findAll(attrs='value')
        soup = subs if subs else [soup]
        contents = []
        for elem in soup:
            if elem.name == 'a' and 'href' in elem.attrs:
                contents.append(elem['href'])
            elif elem.name == 'abbr' and 'title' in elem.attrs:
                contents.append(elem['title'])
            elif elem.name == 'time' and 'datetime' in elem.attrs:
                contents.append(elem['datetime'])
            elif elem.name in ['img', 'area'] and 'alt' in elem.attrs:
                contents.append(elem['alt'])
            else:
                contents.append(self.__getContent(elem, all))
        if not contents:
            return ''
        if sep:
            return sep.join(contents)
        return ''.join(contents)

    def __getContent(self, soup=None, all=False):
        if not soup:
            soup = self._soup
        if soup.string:
            return soup.string.strip().strip('"')
        contents = []
        for elem in soup.contents:
            contents.append(self.__getContent(elem, all))
        if not contents:
            return ''
        if all:
            return ''.join(contents)
        return max(contents, key=len)

class vEvent(vObject):
    ATTR_CONTENT  = ('summary', 'description', 'location', 'category', 'status', 'method', 'uid', 'url')
    ATTR_DATETIME = ('dtstart', 'dtend', 'dtstamp', 'last_modified', 'rdate', 'exdate')
    ATTR_DURATION = ('duration',)
    ATTR_RULE     = ('rrule', 'exrule')

    ATTR_RELATION = {'duration': 'dtstart'}
    ATTR_FALLBACK = {'dtend': 'duration'}

    def __dir__(self):
        return list(self.ATTR_CONTENT + self.ATTR_DATETIME + self.ATTR_RULE)

    def __getattr__(self, attr):
        if attr in self.ATTR_RULE:
            rrule = self._soup.find(attrs=attr)
            value = str(vRule(rrule)) if rrule else None
        elif attr in self.ATTR_DATETIME:
            value = self.getDatetime(attr.replace('_', '-'))
        elif attr in self.ATTR_DURATION:
            value = self.getDuration(attr.replace('_', '-'))
        elif attr in self.ATTR_CONTENT:
            value = self.getContent(attr)
        if not value and attr in self.ATTR_FALLBACK:
            value = getattr(self, self.ATTR_FALLBACK[attr])
        if not attr in list(self.ATTR_CONTENT + self.ATTR_DATETIME + self.ATTR_DURATION + self.ATTR_RULE):
            raise AttributeError
        return value

class vRule(vObject):
    ATTR_KEYS = ('freq', 'interval', 'until', 'count', 'wkst', 'bysetpos', 'bymonth', 'byweekno', 'byyearday', 'bymonthday', 'byday', 'byhour', 'byminute', 'bysecond')
    ATTR_TRIM = {'byday': 2}

    def __str__(self):
        freq = getattr(self, 'freq')
        if freq:
            rrule = self._getRule(freq)
        else:
            rrule = self._getContent()
        return rrule.upper()

    def __dir__(self):
        return list(self.ATTR_KEYS)

    def __getattr__(self, attr):
        if attr in self.ATTR_KEYS:
            value = self.getContent(attr, ',')
        else:
            raise AttributeError
        if attr in self.ATTR_TRIM and value:
            value = value[:self.ATTR_TRIM[attr]]
        return value

    def _getRule(self, freq):
        rrule = 'FREQ=%s' % freq
        for key in self.ATTR_KEYS[1:]:
            value = getattr(self, key)
            if value:
                rrule += ';%s=%s' % (key, value)
        return rrule
