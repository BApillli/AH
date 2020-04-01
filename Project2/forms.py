from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextField, SelectField, DateTimeField)
from wtforms.validators import DataRequired, EqualTo
from wtforms_components import TimeField
from readList import ReadList

class LoginForm(FlaskForm):
    city = SelectField(u'City', choices=ReadList.get_city(), validators=[DataRequired()])
    cuisine = SelectField('Cuisine', choices=ReadList.get_cus(), validators=[DataRequired()])
    day = SelectField('Day', choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
            ('Thur', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], validators=[DataRequired()])
    time = TimeField('Time')
    submit = SubmitField('Submit')

