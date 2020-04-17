from py2neo import Graph
from py2neo import Database
import json
import datetime
import re

graph = Graph("bolt://156.155.137.75:8000", auth=("neo4j", "yelpme"))

def main():
    store = graph.run("MATCH (n:Business) RETURN n").data()

    #temp = is_open("Sunday", "16:30" , "LbM7p-cI0dUCkaUzOyFMTw")
    #print(temp)
    print(get_top_five("AY_cjY1bRAD-I_K11dYvOA", "Scottsdale", "Fast Food", "Monday", "14:00"))
    #businesses = get_buss("Champlain", "Burgers")
    #get_hours("Sunday", "McDonald's")
    #print()
    # you can get stars, location, etc like this:
    # star = cat_buss(store, 2)
    
def best_business(city, day, time, cuisine):
    store = get_buss(city, cuisine)
    business = []
    for i in range(0, len(store)):
        if is_open(day, time, store[i]['m']['id']):
            # stores top business id and name
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
    store = graph.run("MATCH (n:Business {id: \"" + id + "\"}) RETURN n." + day.lower()).evaluate()
    return str(store)

def is_open(day, time, id):
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

#return the list of business ordered by stars
def get_buss(city, cruisine):
    #need to quadrable check
    store = graph.run("MATCH (m:Business)-[:IN_CATEGORY]->(n:Category) WHERE m.city=\""+city+"\" AND n.id=\""+cruisine+"\" RETURN m,n ORDER BY m.stars DESC, m.review_count DESC").data()
    return store

#returns the user and their review -- I MADE CHANGES HERE AS WELL
def most_useful(buss_id):
    #is there a dynamic way to check the last two years.. stay tuned
    store = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE r.date>'2017-12-31' AND n.id=\""+buss_id+"\" RETURN r.useful ORDER BY r.useful DESC, r.date DESC").data()
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
        useful = store[i]['r.useful']
        i += 1
        if (i == len(store)-1):
            break
    #this would mean they all none, so start from beginning- since they're already sorted by date
    if useful is None:
        i = 0
    #if we only have none values to work with it'll return the most recent review...
    
    #this should be okay................................................................
    #it is sorted by date so the more recent one is first anyway.. resolving duplicates. need to test extensively

    if two_years == 0:
        r_review = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE r.date>'2017-12-31' AND n.id=\""+buss_id+"\" RETURN m.name, r.text, r.stars, m.id ORDER BY r.useful DESC, r.date DESC").data()
    else:
        r_review = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE n.id=\""+buss_id+"\" RETURN m.name, r.text, m.id ORDER BY r.useful DESC, r.date DESC").data()  
    
    return r_review[i]

def review_count(business_id):
    count = graph.run("MATCH (m:User)-[r:REVIEWS]->(n:Business) WHERE n.id=\""+business_id+"\" RETURN count(*) as count").data()

    return count

def get_photos(business_id):
    # still need to do condition where there are no photos
    store = graph.run("MATCH (b:Business {id: \"" + business_id + "\"}) - [:PHOTO] -> (p:Photo) return p.id, p.caption").data()
    return store

# i made changes to this
def get_top_five(user_id, city, cuisine, day, time):
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

def get_default_res(city):
    query = "MATCH (f:Business {city: \"" + city + "\"}) RETURN f ORDER by f.stars DESC LIMIT 5"
    restaurants = []
    store = graph.run(query).data()
    for i in range(0, len(store)):
        restaurants.append(store[i]['f'])

    return restaurants

if __name__ == "__main__":
    main()
