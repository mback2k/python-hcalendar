# Inspired by https://github.com/glennjones/UfXtract/blob/master/UfXtractUnitTests/test_hCalendar_3.cs
from ufxtract_setup import UfXtractSetup
import datetime

def timedelta(**kwargs):
    days = kwargs['days'] if 'days' in kwargs else 0
    if 'years' in kwargs:
        days += 365 * kwargs.pop('years')
    if 'months' in kwargs:
        days += 30 * kwargs.pop('months')
    if days:
        kwargs['days'] = days
    return datetime.timedelta(**kwargs) 

class hCalendar3(UfXtractSetup):
    href = 'http://ufxtract.com/testsuite/hcalendar/hcalendar3.htm'

    def test_01(self):
        self.assertEqual(self.data[0][0]['duration'], 'P9M')
        self.assertEqual(self.data[0][0].duration, timedelta(months=9))

        self.assertEqual(self.data[0][0].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][0].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(months=9))

    def test_02(self):
        self.assertEqual(self.data[0][1]['duration'], 'P1Y2M')
        self.assertEqual(self.data[0][1].duration, timedelta(years=1, months=2))

        self.assertEqual(self.data[0][1].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][1].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2))

    def test_03(self):
        self.assertEqual(self.data[0][2]['duration'], 'P1Y2M10D')
        self.assertEqual(self.data[0][2].duration, timedelta(years=1, months=2, days=10))

        self.assertEqual(self.data[0][2].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][2].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10))

    def test_04(self):
        self.assertEqual(self.data[0][3]['duration'], 'P1Y2M10DT20H')
        self.assertEqual(self.data[0][3].duration, timedelta(years=1, months=2, days=10, hours=20))

        self.assertEqual(self.data[0][3].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][3].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=20))

    def test_05(self):
        self.assertEqual(self.data[0][4]['duration'], 'P1Y2M10DT20H30M')
        self.assertEqual(self.data[0][4].duration, timedelta(years=1, months=2, days=10, hours=20, minutes=30))

        self.assertEqual(self.data[0][4].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][4].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=20, minutes=30))

    def test_06(self):
        self.assertEqual(self.data[0][5]['duration'], 'P1Y2M10DT20H30M30S')
        self.assertEqual(self.data[0][5].duration, timedelta(years=1, months=2, days=10, hours=20, minutes=30, seconds=30))

        self.assertEqual(self.data[0][5].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][5].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=20, minutes=30, seconds=30))

    def test_07(self):
        self.assertEqual(self.data[0][6]['duration'], 'P1Y2M10DT20H30M30.5S')
        self.assertEqual(self.data[0][6].duration, timedelta(years=1, months=2, days=10, hours=20, minutes=30, seconds=30.5))

        self.assertEqual(self.data[0][6].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][6].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=20, minutes=30, seconds=30.5))

    def test_08(self):
        self.assertEqual(self.data[0][7]['duration'], 'P1Y2M10DT20.5H')
        self.assertEqual(self.data[0][7].duration, timedelta(years=1, months=2, days=10, hours=20.5))

        self.assertEqual(self.data[0][7].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][7].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=20.5))

    def test_09(self):
        self.assertEqual(self.data[0][8]['duration'], 'P110D')
        self.assertEqual(self.data[0][8].duration, timedelta(days=110))

        self.assertEqual(self.data[0][8].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][8].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(days=110))

    def test_10(self):
        self.assertEqual(self.data[0][9]['duration'], 'PT30M')
        self.assertEqual(self.data[0][9].duration, timedelta(minutes=30))

        self.assertEqual(self.data[0][9].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][9].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(minutes=30))

    def test_11(self):
        self.assertEqual(self.data[0][10]['duration'], 'P0001-02-10')
        self.assertEqual(self.data[0][10].duration, timedelta(years=1, months=2, days=10))

        self.assertEqual(self.data[0][10].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][10].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10))

    def test_12(self):
        self.assertEqual(self.data[0][11]['duration'], 'P0001-02-10T14:30:30')
        self.assertEqual(self.data[0][11].duration, timedelta(years=1, months=2, days=10, hours=14, minutes=30, seconds=30))

        self.assertEqual(self.data[0][11].dtstart, datetime.datetime(year=2007, month=9, day=8))
        self.assertEqual(self.data[0][11].dtend, datetime.datetime(year=2007, month=9, day=8) + timedelta(years=1, months=2, days=10, hours=14, minutes=30, seconds=30))
