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
            except:
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
        except:
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
                except:
                    self.fail("FAIL")
        print("PASSED")    
    
    def test_most_useful(self) :
        print()
        restaurant = get_buss("Scottsdale", "Hot Dogs")
        review = most_useful(restaurant[0]['m']['id'])
        print(restaurant[0]['m']['id'])
        print(review)
        print("... Testing to see if the most useful review is returned ...")        
        print("Test to see if nones are skipped")
        result = {'m.name': 'David', 'm.id': 'TdCeQnHVjA2FgwBnA9lx_g', 'r.text': "Simon's Hot Dogs catered our event in the park and did a TERRIFIC job. They offered a Beef and Vegan Dog and then their Columbia Dog (Pineapple, Mozzarella Cheese, Simon's Sauce, Crushed Potato Chips), German Traditional (Brown Mustard / Fresh Sauerkraut), and Wunderhund (Dill Pickles, Onions, Mustard, Mayo, Peruvian Chiles, and Bacon Bites on Top). The owner of Simons was on hand to take orders and his assistant on the grill. They made our party a GREAT Success and would recommend their catering to anyone who wants a Hot Dog menu event!", 'r.stars': 4.0}
        # try:
        #     self.assertAlmostEqual(result, review)
        #     print("PASSED")
        # except:
        #     self.fail("FAIL")
        
        
        
            