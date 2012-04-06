import re, isodate, datetime

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
                if type(value) is datetime.time:
                    self._datetime[attr] = datetime.datetime.min.replace(hour=value.hour, minute=value.minute, second=value.second, microsecond=value.microsecond, tzinfo=value.tzinfo)
                elif type(value) is datetime.date:
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
