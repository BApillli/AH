from py2neo import Graph
from py2neo import Database
import json
import datetime
import re
import requests

graph = Graph("bolt://35.224.32.106:8000", auth=("neo4j", "yelpme"))

def best_business(city, day, time, cuisine):
    """Returns the best restaurant based on the query.

       Keyword arguments:
       city -- The city the restaurant must be in
       day -- The day of the week that the restaurant must be open on
       time -- The time that the restaurant must be open
       cuisine -- The type of cuisine the restaurant must offer
    """    
    store = get_buss(city, cuisine)
    business = []
    for i in range(0, len(store)):
        if is_open(day, time, store[i]['m']['id']):
            business.append(store[i]['m']['id'])
            business.append(store[i]['m']['name'])
            business.append(store[i]['m']['address'] + ", " + store[i]['m']['city'] + ", " + store[i]['m']['state'])
            business.append(store[i]['m']['stars'])
            business.append(store[i]['m']['latitude'])
            business.append(store[i]['m']['longitude'])
            break
    return business

# for debug purposes    
def all_info(city, day, time, cuisine):
    store = get_buss(city, cuisine)
    business = []
    for i in range(0, len(store)):
        if is_open(day, time, store[i]['m']['id']):
            # stores top business id and name
            business.append(store[i]['m']['id'])
            business.append(store[i]['m']['name'])
            break
    print(" ----- business id -----")    
    print(business[0]) 
    print(" ----- business name -----")
    print(business[1])  
    print(" ----- review -------------")
    review = most_useful(str(business[0]))
    print(review)
    user = review['m.id']
    print("--------- user ---------")
    print(user)
    restaurants = get_top_five(user, city, cuisine, day, time)
    print("--------- restaurants ---------")
    print(restaurants)
    print(" ----- photo ids ----------")
    photos = get_photos(str(business[0]))
    print(photos)
    return restaurants
    
def cat_buss(buss, index):
    entry = buss[index]["n"]
    return entry

def get_hours(day, id):
    """Returns the trading hours of the restaurant on the specified day"""
    store = graph.run("MATCH (n:Business {id: \"" + id + "\"}) RETURN n." + day.lower()).evaluate()
    return str(store)

def is_open(day, time, id):
    """Checks if the restaurant is open at the specified day and time. 
       Returns true if it's open, and false if it is not open.

       Keyword arguments:
       day -- The day of the week
       time -- The time of the day (H:M)
       id -- The id of the restaurant
    """
    hours = get_hours(day, id)
    if hours == "Closed":
        return False
    if hours == "null":
        return None
    opens = datetime.datetime.strptime(hours.split("-")[0], "%H:%M")
    closes = datetime.datetime.strptime(hours.split("-")[1], "%H:%M")
    booking = datetime.datetime.strptime(time, "%H:%M")
    if (opens == closes):
        return True
    if (opens < closes):
        if (booking>=opens and booking <= closes):
            return True
        else:
            return False
    else:
        closes = closes + datetime.timedelta(days=1)
        if (booking>=opens and booking <= closes):
            return True
        else:
            return False

def get_buss(city, cruisine):
    """ Returns list of restaurants ordered by stars in descending order. 

        Keyword arguments:
        city -- The city the restaurant must be in
        cuisine -- The type of cuisine the restaurant must offer
    """  
    store = graph.run("MATCH (m:Business)-[:IN_CATEGORY]->(n:Category) WHERE m.city=\""+city+"\" AND n.id=\""+cruisine+"\" RETURN m,n ORDER BY m.stars DESC, m.review_count DESC").data()
    return store

def most_useful(buss_id):
    """Returns the user with the most useful review as well as the review.

       Keyword arguments:
       buss_id -- The id of the business that the user is reviewing.
    """
    x = get_date()
    store = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE r.date>=\""+x+"\" AND n.id=\""+buss_id+"\" RETURN r.useful ORDER BY r.useful DESC, r.date DESC").data()    

    #no reviews in the past two years- just use the 'recent' one
    two_years = 0
    if (len(store)==0) :
        store = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE n.id=\""+buss_id+"\" RETURN r.useful ORDER BY r.useful DESC, r.date DESC").data()    
        two_years = 1
        #there are cases when a business doesn't have reviews
        if (len(store)==0):
            return None
    i = 0
    useful = store[0]['r.useful']
    #skipping those nones...............................................................
    while (useful is None) :
        i += 1
        if (i == len(store)-1):
            break
        useful = store[i]['r.useful']
    
    #this would mean they all none, so start from beginning- since they're already sorted by date
    if useful is None:
        i = 0
   
    #if we only have none values to work with it'll return the most recent review...

    if two_years == 0:
        r_review = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE r.date>=\""+x+"\" AND n.id=\""+buss_id+"\" RETURN m.name, r.text, r.stars, m.id ORDER BY r.useful DESC, r.date DESC").data()
    else:
        r_review = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE n.id=\""+buss_id+"\" RETURN m.name, r.text, m.id ORDER BY r.useful DESC, r.date DESC").data()  

    return r_review[i]

def review_count(business_id):
    """Returns the review count of a business

       Keyword arguments:
       business_id -- the id of the business
    """   
    count = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE n.id=\""+business_id+"\" RETURN count(*) as count").data()
    return count

def get_photos(business_id):
    """Returns a list of photos of the business

       Keyword arguments:
       business_id -- The id of the business
    """   
    store = graph.run("MATCH (b:Business {id: \"" + business_id + "\"}) - [:PHOTO] -> (p:Photo) return p.id, p.caption").data()
    return store

def get_top_five(user_id, city, cuisine, day, time):
    """Returns the top five restaurants ordered by stars in descending order.

       Keyword arguments:
       user_id -- The id of the user with the most useful review
       city -- The city that the restaurants have to be in
       cuisine -- The cuisine that the restaurants have to offer 
       day -- The day of the week that the restaurants have to be open on
       time -- The time that the restaurants have to be open
    """   
    query = "MATCH (a:User{id: \"" + user_id + "\"}) - [:FRIEND] -> (:User) - [:FRIEND] -> (c:User), (a) - [:FRIEND] -> (b:User) \
            OPTIONAL MATCH (b) - [:REVIEWS] -> (d:Business {city: \"" + city + "\"})-[:IN_CATEGORY]->(:Category {id: \"" + cuisine + "\"}) \
            OPTIONAL MATCH (c) -[:REVIEWS] -> (e:Business {city: \"" + city + "\"})-[:IN_CATEGORY]->(:Category {id: \"" + cuisine + "\"}) \
            WITH collect(d)+collect(e) AS nodez UNWIND nodez as f RETURN DISTINCT f \
            ORDER by f.stars DESC, f.review_count DESC LIMIT 50"
    store = graph.run(query).data()
    
    j = 0
    restaurants = []
    for i in range (0, len(store)):
        if is_open(day, time, store[i]['f']['id']):
            j+=1
            restaurants.append(store[i]['f'])
        if j == 5:
            break    
    return restaurants

def get_default_res(city, id):
    """Returns list of restaurants in a city ordered by stars in descending order.

       Keyword arguments:
       city -- The city that the restaurants have to be in
       id -- The id of the business that cannot be part of the list
    """   
    query = "MATCH (f:Business {city: \"" + city + "\"}) RETURN f ORDER by f.stars DESC LIMIT 6"
    restaurants = []
    j = 0
    store = graph.run(query).data()
    for i in range(0, len(store)):
        if store[i]['f']['id'] != id:
            restaurants.append(store[i]['f'])
            j+=1
        if j == 5:
            break

    return restaurants

def get_date():
    """Returns a date two years prior to the current date"""
    x = str(datetime.datetime.now())
    z = str(int(x[0:4]) - 2)
    y = str(x[4:10])
    z += y
    return z

def is_photo_valid(photos):
    new_photos = []
    for i in range(0, len(photos)):
        response = requests.get(photos[i])
        if response.status_code == 200:
            new_photos.append(photos[i])

    return new_photos    
