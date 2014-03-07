import unittest
import ephemeris

class TestSun(unittest.TestCase):

    def setUp(self):
        pass

    def test_response(self):

        r = ephemeris.sun('!sun')
        print r
        self.assertEqual(type(r), str)
