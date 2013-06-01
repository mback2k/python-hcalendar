from vcalendar import vCalendar
from bs4 import BeautifulSoup

class hCalendar(object):
    def __init__(self, markup, value=None, key='id'):
        if isinstance(markup, BeautifulSoup):
            self._soup = markup
        else:
            self._soup = BeautifulSoup(markup)
        if value:
            self._soup = self._soup.find(**{key: value})
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
