#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .vobject import vObject

class vEvent(vObject):
    ATTR_CONTENT  = ('summary', 'description', 'location', 'category', 'status', 'method', 'uid', 'url')
    ATTR_DATETIME = ('dtstart', 'dtend', 'dtstamp', 'last_modified', 'rdate', 'exdate')
    ATTR_DURATION = ('duration',)
    ATTR_RULE     = ('rrule', 'exrule')
    ATTR_PATH     = ('uid',)

    ATTR_DATETIME_RELATION = {'duration': '+dtstart'}
    ATTR_DATETIME_FALLBACK = {'dtend': 'duration'}

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
            if not value and attr in self.ATTR_PATH:
                value = self.getPath()
        else:
            raise AttributeError('Unknown or unsupported attribute "%s".' % attr)
        return value

class vRule(vObject):
    ATTR_KEYS = ('freq', 'interval', 'until', 'count', 'wkst', 'bysetpos', 'bymonth', 'byweekno', 'byyearday', 'bymonthday', 'byday', 'byhour', 'byminute', 'bysecond')
    ATTR_TRIM = {'byday': 2}

    def __str__(self):
        freq = getattr(self, 'freq')
        if freq:
            rrule = self.getRule(freq)
        else:
            rrule = self.getContentFromSoup()
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

    def getRule(self, freq):
        rrule = 'FREQ=%s' % freq
        for key in self.ATTR_KEYS[1:]:
            value = getattr(self, key)
            if value:
                rrule += ';%s=%s' % (key, value)
        return rrule
