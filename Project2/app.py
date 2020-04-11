from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm
import main
from flask import make_response, request
from config import Config
from datetime import datetime
import csv

app = Flask(__name__)
app.config.from_object(Config)

#making lists we'll possibly need

res_names = ["WhatABurger","Girl & The Goat","Vernick Food & Drink"]
stars = [5,4,3,3,1]
picts = ["../static/images/IMG-4316.JPG","../static/images/IMG-4317.JPG","../static/images/IMG-4318.JPG"]
trading = ["24hrs","16:30 - 22:00","17:00 - 02:00"]
review = "blah blah blah"
name = []

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
            review = main.most_useful(str(name[1]))
            if review != '':

                # gets the user of the review
                user = review['m.id']
                # gets the list of restaurants
                best_buss_rating = name[3]
                restaurants = main.get_top_five(user, form.city.data, form.cuisine.data, form.day.data, form.time.data.strftime("%H:%M"))
                trade = trading_hours(restaurants, form.day.data)
                rating = star_rating(restaurants)
                review = review['r.text']
                address = name[2]
                pictIDs = images(main.get_photos(name[0]))
                #print(rating)
                # returns top restaurant with information followed by list of extra restaurants
                # goes to top restaurant with information followed by list of extra restaurants
                print('SECOND PAGE')
                return render_template('secondpage.html', form=form,len = len(restaurants),res_names=restaurants,stars = rating,pictIDs=pictIDs,trading = trade, review=review, best_res=name[1], address=address, rating=best_buss_rating) 

            else :
                print('THERE IS NO REVIEW')
                # goes to the noresult when there is no review
                address = name[2]
                print('NO REVIEWW')
                return render_template('noresult.html', form=form, title='No Review, thus no extra recommendations :/', best_res=name[1], address=address)
  

        # goes to the noresult page that will cater for the no result
        print('NO RESULTSS')
        return render_template('noresult.html', form=form, title='No Result was found for this, want to try again?', address='', best_res='')

    else:
        #goes to the welcome page
        return render_template('firstpage.html', form=form)

''' for later '''
@app.route('/results', methods = ['GET', 'POST'])
def results(data):
    if form.validate_on_submit():
        flash('User wants a restuarant in the city {}, with the cuisine {}, from the time {}, on the day {}'.format(
            form.city.data, form.cuisine.data, form.time.data, form.day.data))
        name = main.all_info(form.city.data, form.day.data, form.time.data.strftime("%H:%M"), form.cuisine.data)
        return render_template('index.html', form=form,len = len(name),res_names=name,stars = stars,picts = picts,trading = trading)   
    else:
        #just returns hard coded stuff
        return render_template('index.html', form=form,len = len(res_names),res_names=res_names,stars = stars,picts = picts,trading = trading, review=review)

''' Returns the trading hours for the list of restaurants '''
def trading_hours(buss,day):
    hours = []
    for i in range (0, len(buss)):
        hours.append(buss[i][day])
    return hours    

''' Returns the star rating for the list of restaurants '''
def star_rating(buss):
    stars = []
    for i in range(0, len(buss)):
        stars.append(buss[i]['stars'])
    return stars

''' Changes format of photo_id to source strings '''
def images(photos):
    for i in range(0, len(photos)):
        photos[0]['p.id'] = "../static/images/_" + photos[0]['p.id'] + ".JPG"
    return photos    

if __name__ == '__main__':
    app.run(debug=True)