import unittest

from main import *


class TestGetBuss(unittest.TestCase):
    # checks that the restaurants returned is in the required city 
    # and serves the required cruisine
    def test_buss(self):
        hold = get_buss("Champlain", "Burgers")
        for i in range(0, len(hold)-1):
            print(hold[i]["m"])
            self.assertAlmostEqual(hold[i]['m']['city'], "Champlain")
            self.assertAlmostEqual(hold[i]['n']['id'], "Burgers")