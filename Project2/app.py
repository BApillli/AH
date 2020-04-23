from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm
import main
from flask import make_response, request
from config import Config
from datetime import datetime
import csv
import random

app = Flask(__name__)
app.config.from_object(Config)

#making lists we'll possibly need

res_names = ["WhatABurger","Girl & The Goat","Vernick Food & Drink"]
stars = [5,4,3,3,1]
picts = ["../static/images/IMG-4316.JPG","../static/images/IMG-4317.JPG","../static/images/IMG-4318.JPG"]
trading = ["24hrs","16:30 - 22:00","17:00 - 02:00"]
review = "blah blah blah"
name = []
loc = []
empty = 0

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        flash('User wants a restuarant in the city {}, with the cuisine {}, from the time {}, on the day {}'.format(
            form.city.data, form.cuisine.data, form.time.data, form.day.data))
        name = main.best_business(form.city.data, form.day.data, form.time.data.strftime("%H:%M"), form.cuisine.data)

        if len(name) != 0:    
            # gets the review
            review = main.most_useful(str(name[0]))
            if review != '':

                # gets the user of the review
                user = review['m.id']
                # gets the list of restaurants
                best_buss_rating = name[3]
                restaurants = main.get_top_five(user, form.city.data, form.cuisine.data, form.day.data, form.time.data.strftime("%H:%M"))
                if restaurants == []:
                    print("NO LIST OF RESTAURANTS")
                    restaurants = main.get_default_res(form.city.data, name[0])
                    empty = 1
                trade = trading_hours(restaurants, form.day.data)
                rating = star_rating(restaurants)
                review = review['r.text']
                address = name[2]
                extra_addresses = get_addresses(restaurants)
                photos = main.get_photos(name[0])
                pictIDs = main.is_photo_valid(images(photos, name[0]))
                extra_photos = get_extra_photos(restaurants)
                captions = get_captions(photos)
                #latitude and longitude
                locations = get_location(restaurants)
                lenp = 0
                if pictIDs == []:
                    lenp = 1
                    pictIDs.append("./static/images/iu.png") # replace with default image src
                else:
                    lenp = random.randint(1,len(pictIDs)) 
     
                print('SECOND PAGE')
                return render_template('secondpage.html',
                    form=form,
                    len = len(restaurants),
                    res_names=restaurants,
                    empty=empty,
                    stars = rating,
                    pictIDs=pictIDs,
                    lenp = lenp,
                    locations = locations,
                    trading = trade, 
                    review=review, 
                    best_res=name[1], 
                    address=address, 
                    extra_adresses=extra_addresses,
                    extra_photos=extra_photos,
                    rating=best_buss_rating, 
                    captions=captions,
                    htm="second"
                    ) 

            else :
                # goes to the noresult when there is no review
                address = name[2]
                best_buss_rating = name[3]
                print('NO REVIEWW')
                return render_template('noresult.html', form=form, title='No Review, thus no extra recommendations :/', 
                    pg=1, best_res=name[1], address=address, rating=best_buss_rating)
  
        # goes to the noresult page that will cater for the no result
        print('NO RESULTSS')
        return render_template('noresult.html', form=form, title='No Result was found for this, want to try again?', pg=2)

    else:
        #goes to the welcome page
        return render_template('firstpage.html', form=form, htm="first")

def trading_hours(buss,day):
    """Returns the trading hours for the list of restaurants"""
    hours = []
    day = day.lower()
    for i in range (0, len(buss)):
        hours.append(buss[i][day])
    return hours    

def star_rating(buss):
    """Returns the star rating for the list of restaurants"""
    stars = []
    for i in range(0, len(buss)):
        stars.append(buss[i]['stars'])
    return stars

def images(photos, id):
    """Changes format of photo_id to source strings"""
    img = []
    for i in range(0, len(photos)):
        #photos[i]['p.id'] = "../static/photos/" + photos[i]['p.id'] + ".jpg"
        data = "https://s3-media2.fl.yelpcdn.com/bphoto/" + photos[i]['p.id'] + \
        "/o.jpg"
        img.append(data)
    return img  

def get_captions(photos):
    """Gets captions for the images"""
    cap = []
    for i in range(0, len(photos)):
        cap.append(photos[i]['p.caption'])
    return cap    

def get_location(restaurants):
    """gets latitude and longitude for map (2d array)"""
    location = []
    temp = []
    for i in range(0, len(restaurants)):
        temp.append(restaurants[i]['latitude'])
        temp.append(restaurants[i]['longitude'])
        location.append(temp)
        temp=[]
    return location    

def get_extra_photos(restaurants):
    """gets photos for list of restaurants"""
    photos = []
    temp2 = []
    for i in range(0, len(restaurants)):
        temp = main.get_photos(restaurants[i]['id'])
        for j in range (0, len(temp)):
            temp2.append("https://s3-media2.fl.yelpcdn.com/bphoto/" + 
            temp[j]['p.id'] + "/o.jpg")    
        temp2 = main.is_photo_valid(temp2)    
        photos.append(temp2)
        temp2 = []
    return photos    

def get_addresses(restaurants):
    """gets the addresses for the list of restaurants"""
    address = []
    for i in range(0, len(restaurants)):
        address.append(restaurants[i]['address'] + ", " + restaurants[i]['city'] + 
        ", " + restaurants[i]['state'])        
    return address

if __name__ == '__main__':
    app.run(debug=True)
