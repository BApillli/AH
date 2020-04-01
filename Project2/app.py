from flask import Flask, render_template, flash, redirect, url_for
#from app import app
from forms import LoginForm
from flask import Flask, make_response, request
from config import Config

import csv

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Form to be filled requested for user {},'.format(
            form.city.data))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)
    
if __name__ == '__main__':
    app.run(debug=True)


#@app.route('/login', methods=['GET', 'POST'])
#def login():
#return render_template('login.html', form=form)
