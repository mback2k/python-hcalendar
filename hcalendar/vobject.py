#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re, isodate, datetime

class vObject(object):
    REGEX_DATE = re.compile(r'P(\d{4})-(\d{2})-(\d{2})')
    REGEX_DATETIME = re.compile(r'P(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})')

    ATTR_DATETIME_RELATION = {}
    ATTR_DATETIME_FALLBACK = {}

    def __init__(self, soup):
        self._soup = soup
        self._content = {}
        self._datetime = {}
        self._duration = {}

    def __str__(self):
        return str(self._soup)

    def __getitem__(self, attr):
        return self.getContent(attr)

    def getPath(self):
        parents = self._soup.find_parents()
        parents.insert(0, self._soup)
        pathfmt = lambda e: '%s[%d]' % (e.name, len(e.find_previous_siblings()))
        return '.'.join(reversed(list(map(pathfmt, parents))))

    def getDatetime(self, attr):
        if not attr in self._datetime:
            content = self.getContent(attr)
            if content:
                try:
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
                        self._datetime[attr] = datetime.datetime(value.year, value.month, value.day, tzinfo=isodate.parse_tzinfo('Z'))
                    else:
                        self._datetime[attr] = value
                except isodate.ISO8601Error:
                    self._datetime[attr] = None
            elif attr in self.ATTR_DATETIME_FALLBACK:
                fallback_attr = self.ATTR_DATETIME_FALLBACK[attr]
                fallback_value = getattr(self, fallback_attr)
                if fallback_value and fallback_attr in self.ATTR_DATETIME_RELATION:
                    relation_attr = self.ATTR_DATETIME_RELATION[fallback_attr]
                    if relation_attr.startswith('+'):
                        relation_value = getattr(self, relation_attr[1:])
                        fallback_value = relation_value + fallback_value
                    elif relation_attr.startswith('-'):
                        relation_value = getattr(self, relation_attr[1:])
                        fallback_value = relation_value - fallback_value
                    else:
                        relation_value = getattr(self, relation_attr)
                        fallback_value += relation_value
                self._datetime[attr] = fallback_value
            else:
                self._datetime[attr] = None
        return self._datetime[attr]

    def getDuration(self, attr):
        if not attr in self._duration:
            content = self.getContent(attr)
            if content:
                if self.REGEX_DATETIME.match(content):
                    content = self.REGEX_DATETIME.sub(r'P\1Y\2M\3DT\4H\5M\6S', content)
                elif self.REGEX_DATE.match(content):
                    content = self.REGEX_DATE.sub(r'P\1Y\2M\3D', content)
                value = isodate.parse_duration(content)
                if isinstance(value, isodate.duration.Duration):
                    years = datetime.timedelta(days=int(365*value.years))
                    months = datetime.timedelta(days=int(30*value.months))
                    self._duration[attr] = value.tdelta + years + months
                else:
                    self._duration[attr] = value
            else:
                self._duration[attr] = None
        return self._duration[attr]

    def getContent(self, attr, sep=''):
        if not attr in self._content:
            soup = self._soup.find(attrs=attr)
            if not soup:
                return None
            self._content[attr] = self.getContentFromSoup(soup, sep)
        return self._content[attr]

    def getContentFromSoup(self, soup=None, sep=''):
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
                contents.append(''.join(elem.stripped_strings))
        return sep.join(contents)
