import unittest

from main import *


class TestGetBuss(unittest.TestCase):
    # checks that the restaurants returned is in the required city 
    # and serves the required cruisine
    def test_buss(self):
        hold = get_buss("Champlain", "Burgers")
        sort = []
        for i in range(0, len(hold)):
            self.assertAlmostEqual(hold[i]['m']['city'], "Champlain")
            self.assertAlmostEqual(hold[i]['n']['id'], "Burgers")
            sort.append(hold[i]['m']['stars'])
        #checks if it is ordered by stars    
        sort1 = sort
        sort1 = sorted(sort1, reverse=True)
        self.assertAlmostEqual(sort1, sort)
               
        
            