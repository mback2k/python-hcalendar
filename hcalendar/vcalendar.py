#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .vevent import vEvent

class vCalendar(object):
    def __init__(self, soup):
        self._soup = soup
        self._events = list(map(vEvent, self._soup.findAll(attrs='vevent')))

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
