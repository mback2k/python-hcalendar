from hcalendar import hCalendar
import unittest

try:
    import urllib.request as urllib2
except:
    import urllib2

class UfXtractSetup(unittest.TestCase):
    def setUp(self):
        self.file = urllib2.urlopen(urllib2.Request(self.href, headers={'User-agent': 'Python hCalendar UnitTest'}))
        self.data = hCalendar(self.file, 'uf')

    def tearDown(self):
        self.data = None
        self.file.close()
        self.file = None

    def test_hcalendar(self):
        self.assertTrue(self.data is not None)

    def test_vcalendar(self):
        self.assertTrue(self.data[0] is not None)
