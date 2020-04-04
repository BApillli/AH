from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms_components import TimeField
from readList import ReadList

class LoginForm(FlaskForm):
        """ A class to create the input form """
        city = SelectField('City', default = '', choices=[('', 'City'),] + ReadList.get_city(), validators=[DataRequired()])
        cuisine = SelectField('Cuisine', choices=[('', 'Cuisine'),] + ReadList.get_cus(), validators=[DataRequired()])
        day = SelectField('Day', choices=[('', 'Day'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
                ('Thur', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], validators=[DataRequired()])
        time = TimeField('Time',validators=[DataRequired()])
        submit = SubmitField('Submit')