import unittest

from main import *


class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()

class TestMain(unittest.TestCase):
    """ Test function to verify project requirements for best restaurant
        returned is correct
    """

    def test_get_buss(self):
        hold = get_buss("Scottsdale", "Hot Dogs")
        sort = []

        # checks cruisine and city
        print("[test_get_buss]: tests [1] city, [2] cruisine, [3] stars condition, [4] review count condition") 
        for i in range(0, len(hold)):
            try:
                self.assertAlmostEqual(hold[i]['m']['city'], "Scottsdale")
            except:
                self.fail("FAILED")
            self.assertAlmostEqual(hold[i]['n']['id'], "Hot Dogs")
            sort.append(hold[i]['m']['stars'])
        print("PASSED")

        #checks if it is ordered by stars   
        sort1 = sort
        sort1 = sorted(sort1, reverse=True)
        try:
            self.assertAlmostEqual(sort1, sort)
            print("PASSED")
        except:
            self.fail("FAIL")

        #check if ties are broken
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
        """ Test function to verify we are receiving the correct review based on
            project requirement- checked against the neo4j database
        """

        print()
        restaurant = get_buss("Scottsdale", "Hot Dogs")
        review0 = most_useful(restaurant[0]['m']['id'])
              
        print("[test_most_useful]: none review values are skipped")
        result0 = {'m.name': 'David', 'm.id': 'TdCeQnHVjA2FgwBnA9lx_g', 'r.text': "Simon's Hot Dogs catered our event in the park and did a TERRIFIC job. They offered a Beef and Vegan Dog and then their Columbia Dog (Pineapple, Mozzarella Cheese, Simon's Sauce, Crushed Potato Chips), German Traditional (Brown Mustard / Fresh Sauerkraut), and Wunderhund (Dill Pickles, Onions, Mustard, Mayo, Peruvian Chiles, and Bacon Bites on Top). The owner of Simons was on hand to take orders and his assistant on the grill. They made our party a GREAT Success and would recommend their catering to anyone who wants a Hot Dog menu event!", 'r.stars': 4.0}
        try:
            self.assertAlmostEqual(result0, review0)
            print("PASSED")
        except:
            self.fail("FAIL")
        print()    
        review1 = most_useful('LAoSegVNU4wx4GTA8reB6A')

        print("[test_most_useful]: nones that have a more recent date takes priority")
        result1 = {'r.text': "The truck showed up 44 min early. They still weren't ready. Its upsetting if you are not able to offer the items at least compensate your consumer. A soad cost .50 this could be seen as a sign of good faith. I won't be spending any money or time with them. I cant stress enough how one bad encounter can ruin your rep moving forward. Take care of your customers and they will remember you. I'm not suggesting that you have to give me free stuff but you do have to make some attempt at doing something other then I'm sorry. That tells me you make enough money to not care about me and my $15. Not attemp at anything, no empathy, nothing.", 'm.id': '37jU24vRukJb0ykfTJpghg', 'r.stars': 1.0, 'm.name': 'Clinton'} 
        try:
            self.assertAlmostEqual(result1, review1)
            print("PASSED")
        except:
            self.fail("FAILED")

    def test_is_open(self):
        """ Test function to verify that our function returns the correct boolean
            expression for when a restaurant is open or not based on user input
        """

        print()
        print("[test_is_open]: restaurant is open at a specified time")
        try:
            self.assertTrue(is_open('Saturday', '11:00', 'khxjYMwb_V8UovvwPVhysw'))
            print("PASSED")
        except:
            self.fail("FAILED")

        print()
        print("[test_is_open]: restaurant is closed at a specified time")
        try:
            self.assertFalse(is_open('Sunday', '11:00', 'khxjYMwb_V8UovvwPVhysw'))
            print("PASSED")
        except:
            self.fail("FAILED")

    def test_get_photos(self):
        """
            Test function to check if the correct photo urls are returned- (compared to
            database data) and if we are removing invalid urls correctly
        """
        print()
        print('[test_get_photos]: should return an empty list')
        try:
            self.assertAlmostEqual(get_photos('7f_Z7-b4wwRZ2BPH9x-A3A'), [])
            print("PASSED")
        except:
            self.fail("FAILED")
        
        print()
        print('[test_get_photos]: correct urls are returned')
        photos0 = get_photos("xTKcIQ90mluHH0HGO-sVig")
        try:
            self.assertAlmostEqual(photos0, [{'p.id': 'uE-6bBrl8Dks4_DDDtrOTQ', 'p.caption': ''}, {'p.id': 'MkBaQ15S1dZxkDmNF_JAGw', 'p.caption': ''}])
            print("PASSED")
        except:
            self.fail("FAILED")
        
        print()
        print('[test_get_photos]: elimination of invalid urls')
        
        photos = []
        for i in range(len(photos0)):
            photos.append('https://s3-media2.fl.yelpcdn.com/bphoto/')
            photos[i] += photos0[i]['p.id'] + '/o.jpg'
            
        photos = is_photo_valid(photos)
        try:
            self.assertAlmostEqual(photos, ['https://s3-media2.fl.yelpcdn.com/bphoto/uE-6bBrl8Dks4_DDDtrOTQ/o.jpg', 'https://s3-media2.fl.yelpcdn.com/bphoto/MkBaQ15S1dZxkDmNF_JAGw/o.jpg'])
            print("PASSED")
        except:
            self.fail("FAILED")

    def test_get_top_five(self):
        ''' Test function to verify that the new restaurant recommendations meets the user's
            requirements
        '''

        print()
        print('[test_get_top_five]: tests [1] city, [2] cruisine, [3] stars condition, [4] review count condition')

        restaurants = get_top_five('AY_cjY1bRAD-I_K11dYvOA', 'Scottsdale', 'Fast Food', 'Monday', '12:00')
        # testing to see if the restaurants are in the same city and satisfies the required cruisine
        sort = []
        for i in range(0, len(restaurants)):
            try:
                self.assertAlmostEqual(restaurants[i]['city'], "Scottsdale")
            except:
                self.fail("FAILED")
            sort.append(restaurants[i]['stars'])
        print("PASSED")        
        
        #checks if it is ordered by stars   
        sort1 = sort
        sort1 = sorted(sort1, reverse=True)
        try:
            self.assertAlmostEqual(sort1, sort)
            print("PASSED")
        except:
            self.fail("FAIL")

        #check if ties are broken
        for i in range(0, len(restaurants)):
            # checking the last one against nothing
            if i+1 == len(restaurants):
                break
            if restaurants[i]['stars'] == restaurants[i+1]['stars']:
                a = restaurants[i]['review_count']
                b = restaurants[i+1]['review_count']
                try:
                    self.assertGreaterEqual(a, b)
                except:
                    self.fail("FAIL")
        print("PASSED")         

