#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from .ufxtract_hcalendar1 import hCalendar1
from .ufxtract_hcalendar3 import hCalendar3

if __name__ == '__main__':
    unittest.main()
