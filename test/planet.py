import unittest
from astronomy import planets
import ephem
import datetime
import pytz

local_tz = pytz.timezone('US/Pacific')


class TestPlanet(unittest.TestCase):
    """Data from <http://aa.usno.navy.mil/data/docs/RS_OneDay.php>

    Location: Porland (45.5, 122.7)

    Date: 1 January 2000        Pacific Standard Time

                 SUN
    Begin civil twilight       7:17 a.m.
    Sunrise                    7:51 a.m.
    Sun transit               12:14 p.m.
    Sunset                     4:37 p.m.
    End civil twilight         5:12 p.m.
    """


    def setUp(self):

        self.sol = planets.Sol
        self.sol.set_now(datetime.datetime(2000,1,1))

        portland = ephem.Observer()
        portland.lat = "45.5"
        portland.lon = "-122.7"
        portland.elevation = 50
        self.sol.set_observer(portland)


    def test_sunrise(self):
        
        actual_rise = datetime.datetime(2000,1,1, 7, 51, 00, tzinfo=local_tz)
        rise = self.sol.risetime().astimezone(local_tz)

        # sunrise within two minutes of historical data
        self.assertLess((actual_rise - rise).seconds, 120)
