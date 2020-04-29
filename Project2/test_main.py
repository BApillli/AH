import unittest

from main import *


class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()

class TestMain(unittest.TestCase):
    # checks that the restaurants returned is in the required city 
    # and serves the required cruisine
    def test_buss(self):
        hold = get_buss("Scottsdale", "Hot Dogs")
        #hold = get_buss("Champlain", "Burgers")
        sort = []

        # checks cruisine and city
        print("... Test to check whether it is in the required city and returns the required cruisine ...") 
        for i in range(0, len(hold)):
            try:
                self.assertAlmostEqual(hold[i]['m']['city'], "Scottsdale")
            except ThatException:
                self.fail("FAILED")
            self.assertAlmostEqual(hold[i]['n']['id'], "Hot Dogs")
            sort.append(hold[i]['m']['stars'])
        print("PASSED")
        #checks if it is ordered by stars
        print()
        print("... Test to check whether it is ordered by stars ...")    
        sort1 = sort
        sort1 = sorted(sort1, reverse=True)
        try:
            self.assertAlmostEqual(sort1, sort)
            print("PASSED")
        except ThatException:
            self.fail("FAIL")

        #check if ties are broken
        print()
        print("... Test to check if ties are broken ...") 

        hold2 = get_buss("Scottsdale", "Hot Dogs")
        for i in range(0, len(hold2)):
            # checking the last one against nothing
            if i+1 == len(hold2):
                break
            if hold2[i]['m']['stars'] == hold2[i+1]['m']['stars']:
                a = hold2[i]['m']['review_count']
                b = hold2[i+1]['m']['review_count']
                try:
                    self.assertGreaterEqual(a, b)
                except ThatException:
                    self.fail("FAIL")
        print("PASSED")    
    
    def test_most_useful(self) :
        print()
        restaurant = get_buss("Scottsdale", "Hot Dogs")
        review = most_useful(restaurant[0]['m']['id'])
        print("Testing to see if the most useful review is returned")
        print()
        

        # for i in range(0, len(restaurant)) :
        #     sort.append(restaurant[i]['m']['stars'])
        # sort1 = sorted(sort, reverse=True)
        
        
            