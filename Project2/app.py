from flask import Flask, render_template, flash, redirect, url_for
#from app import app
from forms import LoginForm
from flask import Flask, make_response, request
from config import Config

import csv

app = Flask(__name__)
app.config.from_object(Config)

#making lists we'll possibly need

res_names = ["WhatABurger","Girl & The Goat","Vernick Food & Drink"]
stars = [5,4,3,3,1]
picts = ["../static/images/IMG-4316.JPG","../static/images/IMG-4317.JPG","../static/images/IMG-4318.JPG"]
trading = ["24hrs","16:30 - 22:00","17:00 - 02:00"]

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Form to be filled requested for user {},'.format(
            form.city.data))
        return redirect(url_for('index'))
    return render_template('index.html', form=form,len = len(res_names),res_names = res_names,stars = stars,picts = picts,trading = trading)
    
if __name__ == '__main__':
    app.run(debug=True)


#@app.route('/login', methods=['GET', 'POST'])
#def login():
#return render_template('login.html', form=form)
