# Inspired by https://github.com/glennjones/UfXtract/blob/master/UfXtractUnitTests/test_hCalendar_1.cs
from ufxtract_setup import UfXtractSetup
import datetime

class hCalendar1(UfXtractSetup):
    href = 'http://ufxtract.com/testsuite/hcalendar/hcalendar1.htm'

    def test_01(self):
        self.assertEqual(self.data[0][0].summary, 'Barcamp Brighton 1')

    def test_02(self):
        self.assertEqual(self.data[0][0]['duration'], 'P2D')
        self.assertEqual(self.data[0][0].duration, datetime.timedelta(days=2))

    def test_03(self):
        self.assertEqual(self.data[0][0]['dtstart'], '2007-09-08')
        self.assertEqual(self.data[0][0].dtstart, datetime.datetime(year=2007, month=9, day=8))

    def test_04(self):
        self.assertEqual(self.data[0][0]['dtend'], '2007-09-09')
        self.assertEqual(self.data[0][0].dtend, datetime.datetime(year=2007, month=9, day=9))

    def test_05(self):
        self.assertEqual(self.data[0][0].location, 'Madgex Office, Brighton')

    def test_06(self):
        self.assertEqual(self.data[0][0].description, 'Barcamp is an ad-hoc gathering born from the desire to share and learn in an open environment.')

    def test_07(self):
        self.assertEqual(self.data[0][0].url, 'http://www.barcampbrighton.org/')

    def test_08(self):
        self.assertEqual(self.data[0][0]['class'].lower(), 'public')

    def test_09(self):
        self.assertEqual(self.data[0][0]['dtstamp'], '2007-05-01')
        self.assertEqual(self.data[0][0].dtstamp, datetime.datetime(year=2007, month=5, day=1))

    def test_10(self):
        self.assertEqual(self.data[0][0]['last-modified'], '2007-05-02')
        self.assertEqual(self.data[0][0].last_modified, datetime.datetime(year=2007, month=5, day=2))

    def test_11(self):
        self.assertEqual(self.data[0][0].uid, 'guid1.example.com')

    def test_12(self):
        self.assertEqual(self.data[0][0].status.lower(), 'confirmed')

# TODO: Implement geo location support        
#    def test_13(self):
#        self.assertIsNotNone(self.data[0][0].geo)

# TODO: Implement contact support (hCard)
#    def test_14(self):
#        self.assertIsNotNone(self.data[0][0].contact)

# TODO: Implement organizer support (hCard)
#    def test_15(self):
#        self.assertIsNotNone(self.data[0][0].organizer)
