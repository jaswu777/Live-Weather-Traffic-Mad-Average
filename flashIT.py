from flask import Flask, render_template, jsonify, url_for, request
import json, requests, urllib2, time, datetime, calendar
template = Flask(__name__, static_url_path='', static_folder='Templates') 

@template.route("/")
def zero_one():
	return "The original. This is NOT an error message. This works!"

@template.route("/testing")
def first_one():
	return "It worked!"

@template.route("/namecheap")
def second_one():
	return "This works too!" #render_template('doesntexist.html')

@template.route("/winning")
def third_one():
	return render_template('bigtest1.html')

@template.route("/variable/")
@template.route("/variable/<id>")
def variable_test(id = None):
	if id == None:
		return "No id has been posted"
	else:
		return "Your link url id is " + id

@template.route("/interactivity/")
@template.route("/interactivity/<snippet>")
def test_interactive(snippet = None):
	return render_template('interactivity.html',snippet = snippet)

@template.route("/api_image_recognition_test/")
@template.route("/api_image_recognition_test/<type>/<first_url>/<second_url>/<third_url>")
def image_api(type = None, first_url = None, second_url = None, third_url = None):
	if type == None or first_url == None or second_url == None or third_url == None:
		return "Error in your variables in the secret url"
	else :
		data_type = type
		data_type = data_type.lower()
		url = "http://" + first_url + "." + second_url + "/" + third_url
		api_key = "62ba764dd76e8ba389aeb04dbd637010521bed4a"
		hmac = "03582dd1eaa5372d63ac5f67f17b0b7d9195cf3d"
		return "Wait for now. It works. Wait to parse all of this and output it."

		#r = requests.post(data_type,url,api_key,hmac) -> 2 at most taken. 4 provided.

		#return json.dumps(r.json(), indent = 4) -> valid only if the above line "r" is valid.
		#...WAIT for full SDK API from www.pictorria.com

@template.route("/api_weather_test/")
@template.route("/<name>/api_weather_test/")
@template.route("/api_weather_test/<city>/")
@template.route("/<name>/api_weather_test/<city>")
@template.route("/api_weather_test/<city>/<country>")
@template.route("/<name>/api_weather_test/<city>/<country>")
@template.route("/api_weather_test/<city>/<state>/<country>")
@template.route("/<name>/api_weather_test/<city>/<state>/<country>")
@template.route("/api_weather_test/<street>/<city>/<state>/<country>")
@template.route("/<name>/api_weather_test/<street>/<city>/<state>/<country>")		
def weather(city = None, country = None, street = "", state = "", name = "Random Person!"):
	if city == None or country == None:
		return "Please enter a city name and country name and/or street name and/or state/region name into the url above. For spaces, enter \"_\" underscores. Thank you."
	else:
		now = datetime.datetime.now()
		time_other = now.strftime("%M %p")
		hour = now.strftime("%H")
		if int(hour) > 12:
			hour = int(hour) - 12
		elif int(hour) == 00:
			hour = 12
		time_other = str(hour) + ":" + time_other
		current_time = now.strftime("%d/%m/%Y %H:%M")
		timestamp = time.mktime(time.strptime(current_time, "%d/%m/%Y %H:%M")) * 1.000013000000000000000000000000000000000009
		location_total = street + "," + city + "," + state + "," + country
		google_url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + location_total + "&sensor=false"
		google_data = json.loads(urllib2.urlopen(google_url).read())
		proceed = google_data["status"]
		if proceed == "OK":
			address = google_data["results"][0]["formatted_address"]
			latitude = google_data["results"][0]["geometry"]["location"]["lat"]
			longitude = google_data["results"][0]["geometry"]["location"]["lng"]
			google_time = "https://maps.googleapis.com/maps/api/timezone/json?location=" + str(latitude) + "," + str(longitude) + "&timestamp=" + str(timestamp) + "&sensor=false"
			new_timestamp = json.loads(urllib2.urlopen(google_time).read())
			if new_timestamp["status"] == "OK":
				timezone = new_timestamp["timeZoneName"]
				local_time = timestamp + new_timestamp["dstOffset"] + new_timestamp["rawOffset"]
				converted_hour = time.strftime("%H", time.localtime(local_time))
				if int(converted_hour) > 12:
					converted_hour = int(converted_hour) - 12
				elif int(converted_hour) == 00:
					converted_hour = 12
				converted_minutes = time.strftime("%M", time.localtime(local_time))
				converted_sign = time.strftime("%p", time.localtime(local_time))
				converted_date = time.strftime("%m/%d/%Y", time.localtime(local_time))
				total_time_convert = str(converted_date) + " " + str(converted_hour) + ":" + str(converted_minutes) + " " + str(converted_sign)
			else:
				total_time_convert = " Unknown local time for the location entered"
				timezone = " Unknown timezone"
			map_view = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(latitude) +"," + str(longitude) + "&zoom=17&size=600x300&maptype=hybrid&markers=color:blue|label:D|" + str(latitude) + "," + str(longitude) + "&sensor=false"
			url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(latitude) + "&lon=" + str(longitude) + "&APPID=b1d4941443746120628c3e81b029fabf"
			data = json.loads(urllib2.urlopen(url).read())
			length = len(data["list"])
			traffic_link = "https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"
			weather_layer = "https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=weather"
			temp_temperature = 0
			for j in range(0, length):
				temp_temperature += (1.8 * (data["list"][j]["main"]["temp"] - 273) + 32)
			average_temperature = float(temp_temperature)/float(length)
			average_temperature = str(average_temperature)[0:5]
			average_temperature = float(average_temperature)
			return render_template('weatherFormat.html', weather = data, length = length, time = time_other, address = address, name = name, map = map_view, localtime = total_time_convert, timezone = timezone, latitude = latitude, longitude = longitude, traffic = traffic_link, weatherlayer = weather_layer, average = average_temperature)
			#return jsonify(data) # -> in a json format
		else:
			return render_template('ErrorMessage.html', name = name)

@template.route("/live_weather_traffic/")
def weather_form():
	return render_template('weatherForm.html') 

@template.route("/live_weather_traffic/", methods = ['POST'])
def real_weather():
	name = request.form['name']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	country = request.form['country']
	street = street.replace(" ", "_")
	city = city.replace(" ", "_")
	state = state.replace(" ", "_")
	country = country.replace(" ", "_")
	if name == "" or name == None:
		name = "Random Person"
	if city == None or country == None or city == "" or country == "":
		return "ERROR please go back and try again!"
	else:
		now = datetime.datetime.now()
		time_other = now.strftime("%M %p")
		hour = now.strftime("%H")
		if int(hour) > 12:
			hour = int(hour) - 12
		elif int(hour) == 00:
			hour = 12
		time_other = str(hour) + ":" + time_other
		current_time = now.strftime("%d/%m/%Y %H:%M")
		timestamp = time.mktime(time.strptime(current_time, "%d/%m/%Y %H:%M")) * 1.00001035 # For daylight savings time...
		# * 1.000013000000000000000000000000000000000009 <-- old decimal number time to mutiply before BEFORE daylights saving JUMPING BACK 1 HOUR
		location_total = street + "," + city + "," + state + "," + country
		google_url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + location_total + "&sensor=false"
		google_data = json.loads(urllib2.urlopen(google_url).read())
		proceed = google_data["status"]
		if proceed == "OK":
			address = google_data["results"][0]["formatted_address"]
			latitude = google_data["results"][0]["geometry"]["location"]["lat"]
			longitude = google_data["results"][0]["geometry"]["location"]["lng"]
			google_time = "https://maps.googleapis.com/maps/api/timezone/json?location=" + str(latitude) + "," + str(longitude) + "&timestamp=" + str(timestamp) + "&sensor=false"
			new_timestamp = json.loads(urllib2.urlopen(google_time).read())
			if new_timestamp["status"] == "OK":
				timezone = new_timestamp["timeZoneName"]
				local_time = float(timestamp) + float(new_timestamp["dstOffset"]) + float(new_timestamp["rawOffset"]) 
				converted_hour = time.strftime("%H", time.localtime(local_time))
				converted_hour = int(converted_hour)
				# Temporary fix. A pretty reliable one compared to the last mutiply by this weird long decimal number... + 4!
				if int(converted_hour) > 12:
					converted_hour = int(converted_hour) - 12
				elif int(converted_hour) == 00:
					converted_hour = 12
				converted_minutes = time.strftime("%M", time.localtime(local_time))
				converted_sign = time.strftime("%p", time.localtime(local_time))
				converted_date = time.strftime("%m/%d/%Y", time.localtime(local_time))
				total_time_convert = str(converted_date) + " " + str(converted_hour) + ":" + str(converted_minutes) + " " + str(converted_sign)
			else:
				total_time_convert = " Unknown local time for the location entered"
				timezone = " Unknown timezone"
			map_view = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(latitude) +"," + str(longitude) + "&zoom=17&size=600x300&maptype=hybrid&markers=color:blue|label:D|" + str(latitude) + "," + str(longitude) + "&sensor=false"
			url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(latitude) + "&lon=" + str(longitude) + "&APPID=b1d4941443746120628c3e81b029fabf"
			data = json.loads(urllib2.urlopen(url).read())
			length = len(data["list"])
			traffic_link = "https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"
			weather_layer = "https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=weather"
			temp_temperature = 0
			for j in range(0, length):
				temp_temperature += (1.8 * (data["list"][j]["main"]["temp"] - 273) + 32)
			average_temperature = float(temp_temperature)/float(length)
			average_temperature = str(average_temperature)[0:5]
			average_temperature = float(average_temperature)
			return render_template('weatherFormat.html', weather = data, length = length, time = time_other, address = address, name = name, map = map_view, localtime = total_time_convert, timezone = timezone, latitude = latitude, longitude = longitude, traffic = traffic_link, weatherlayer = weather_layer, average = average_temperature)
			#return jsonify(data) # -> in a json format
		else:
			return render_template('ErrorMessage.html', name = name)

if __name__ == '__main__':
	template.run(debug = False) #Set debug to False for production purposes