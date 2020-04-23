import unittest

from main import *


class TestGetBuss(unittest.TestCase):
    # checks that the restaurants returned is in the required city 
    # and serves the required cruisine
    def test_buss(self):
        hold = get_buss("Champlain", "Burgers")
        sort = []

        # checks cruisine and city
        print("... Test to check whether it is in the required city and returns the required cruisine ...") 
        for i in range(0, len(hold)):
            self.assertAlmostEqual(hold[i]['m']['city'], "Champlain")
            self.assertAlmostEqual(hold[i]['n']['id'], "Burgers")
            sort.append(hold[i]['m']['stars'])
        
        #checks if it is ordered by stars
        print("... Test to check whether it is ordered by stars ...")    
        
        sort1 = sort
        sort1 = sorted(sort1, reverse=True)
        self.assertAlmostEqual(sort1, sort)
        
        #check if ties are broken
        print("... Test to check if ties are broken ...") 

        hold2 = get_buss("Scottsdale", "Hot Dogs")
        for i in range(0, len(hold2)):
            # checking the last one against nothing
            if i+1 == len(hold2):
                break
            if hold2[i]['m']['stars'] == hold2[i+1]['m']['stars']:
                a = hold2[i]['m']['review_count']
                b = hold2[i+1]['m']['review_count']
                #print("a is "+ str(a ) + " b is " + str(b))
                self.assertGreaterEqual(a, b)

        
            