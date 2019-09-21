import os
import json
import time
import random
import logging
import functools
import google.oauth2.credentials
import googleapiclient.discovery

from .models import db, User, Sensor
from application import login
from .form import SensorForm
from datetime import datetime as dt
from flask import current_app as app
from authlib.client import OAuth2Session
from flask import Flask, render_template, url_for, redirect, request, make_response, Response

random.seed()
room_temperature = 25 	# in celcius
temp_delta = 5			# offset from room_temperature
TIME_DELTA = 5			# 1 measurement/ time_delta in seconds
SENSOR_MEMORY = 1		# in hours

# App routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/home")
def home():
	if login.is_logged_in():
		return render_template('home.html')
	return redirect(url_for('index'))

@app.route("/dash")
def dash():
	if login.is_logged_in():
		user_info = login.get_user_info()
		username_ = user_info['name']
		email_ = user_info['email']
		pic = user_info['picture']
		if username_ and email_:
			existing_user = User.query.filter(User.email == email_).first()
			if existing_user:
				app.logger.info(f'{username_} ({email_}) already created!')
				num_sensor = Sensor.query.filter(Sensor.uid == existing_user.id).count()
				return render_template('dash.html', username=username_, picture=pic, num_sensors=num_sensor)
			else:
				new_user = User(username=username_,\
								email=email_,\
								created=dt.now(),\
								picture=pic)
				app.logger.info(f'new {username_} ({email_}) created! and added to database')
				db.session.add(new_user)
				db.session.commit()
	return make_response(f"{new_user} successfully created!")

@app.route("/registerSensor", methods=['GET', 'POST'])
def registerSensor():
	if login.is_logged_in():
		user_info = login.get_user_info()
		email_ = user_info['email']
		cur_uid = User.query.filter(User.email == email_).first().id
		form = SensorForm()
		if form.validate_on_submit():
			sensor_name = form.sname.data
			sensor_type = "Humidity" if form.stype.data else "Temperature"
			existing_sensor = Sensor.query.filter(Sensor.sname == sensor_name, Sensor.stype == form.stype.data).first()
			if not(existing_sensor):
				new_sensor = Sensor(sname=sensor_name, stype=form.stype.data, uid=cur_uid)
				app.logger.info(f'A sensor named {sensor_name} created! and associated to user: {email_} in database')
				print(new_sensor)
				exist = "sensor created"
				db.session.add(new_sensor)
				db.session.commit()
				return redirect(url_for('home'))
			else:
				print('Sensor, already exists, Try different name or type')
				exist = "Sensor, already exists, Try different name or type"
				return render_template('form.html', form=form, exists=exist)			
	return render_template('form.html', form=form)

@app.route("/temp")
def temp():
	if login.is_logged_in():
		return render_template('temp.html')

@app.route("/temp_sensor_data")
def temp_sensor_data():
	def generate_random_data():
		counter = 1
		while(True):
			json_data = json.dumps({'time': dt.now().strftime('%Y-%m-%d %H:%M:%S'),\
									'value': room_temperature + random.uniform(-1,1)*temp_delta})
			yield f"data:{json_data}\n\n"
			time.sleep(TIME_DELTA)
			counter += 1
			if (counter%(SENSOR_MEMORY*((60*60)/TIME_DELTA)) == 0):
				continue
	return Response(generate_random_data(), mimetype='text/event-stream')


@app.route("/hum")
def hum():
	if login.is_logged_in():
		return "fUbAr"

if __name__ == '__main__':
    app.run(debug=True)
