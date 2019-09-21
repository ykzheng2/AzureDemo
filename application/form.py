from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SensorForm(FlaskForm):
	sname = StringField('Sensor Name', validators=[DataRequired()])
	stype = BooleanField('Humidity (default Sensor: Temperature)')
	submit = SubmitField('Add Sensor')