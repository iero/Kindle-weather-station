#!/usr/bin/python
# encoding=utf-8
# -*- coding: utf-8 -*-

# Author : Greg Fabre - http://www.iero.org
# Public domain source code
# Published March 2015
# Update October 2016

# This code creates an SVG image, ready for Kindle 600x800 screen.
# With weather information from Netatmo weather station and 
# forecast from forecast.io.

# Please fill settings.xml file

import math
import time
import datetime
import locale
import lnetatmo
import requests
import geticon
import xml.etree.ElementTree as ET

locale.setlocale(locale.LC_TIME,'')

params_file="settings.xml"
filename = "ieroStation.svg"

# Create 

# parse params file
tree = ET.parse(params_file)
root = tree.getroot()
for service in root.findall('service'):
	if service.get('name') == 'station' :
		city=service.find('city').text
	elif service.get('name') == 'darksky' :
		api_key=service.find('api_key').text
		lat=service.find('lat').text
		lng=service.find('lng').text
		units=service.find('units').text
	elif service.get('name') == 'wunderground' :
		wu_api_key=service.find('api_key').text
		wu_lat=service.find('lat').text
		wu_lng=service.find('lng').text
	elif service.get('name') == 'netatmo' :
		indoor=service.find('indoor').text
		outdoor=service.find('outdoor').text
		pluvio=service.find('raingauge').text


# Dark sky
darkaddress = 'https://api.darksky.net/forecast/'+api_key+'/'+lat+','+lng+'?lang=fr&units=si&exclude=flags'
darkdata = requests.get(darkaddress).json()

# get netatmo data

authorization = lnetatmo.ClientAuth()
devList = lnetatmo.DeviceList(authorization)

# Create SVG file

svg_file = open(filename,"w")

svg_file.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
svg_file.write('<svg xmlns="http://www.w3.org/2000/svg" height="800" width="600" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
svg_file.write('<g font-family="Chalkboard">\n')
#svg_file.write('<g>\n')

# Parsing values

maintenant=time.strftime('%d/%m/%y %H:%M',time.localtime())
svg_file.write('<text style="text-anchor:start;" font-size="30px" x="20" y="40">')
svg_file.write(city)
svg_file.write(', le ')
svg_file.write("%s" % (maintenant))
svg_file.write('</text>\n')

rain1 = 0
rain24 = 0
for module, moduleData in devList.lastData(exclude=3600).items() :
	if module == indoor :
		for sensor, value in moduleData.items() :
			if sensor == 'Temperature' :
				tempEntier=math.floor(value)
				tempDecimale=10*(value - tempEntier)
				svg_file.write('<text style="text-anchor:end;" font-size="80px" x="460" y="750">')
				svg_file.write("%i" % (tempEntier))
				svg_file.write('</text>\n')
				svg_file.write('<text style="text-anchor:start;" font-size="40px" x="460" y="750">,')
				svg_file.write("%i" % (tempDecimale))
				svg_file.write('</text>\n')
				svg_file.write('<circle cx="480" cy="700" r="7" stroke="black" stroke-width="3" fill="none"/>')
				svg_file.write('<text style="text-anchor:start;" font-size="35px" x="490" y="715">C</text>')
			elif sensor == 'Pressure' :
				svg_file.write('<text style="text-anchor:start;" font-size="30px" x="430" y="210">')
				svg_file.write("%i hPa" % (round(value)))
				svg_file.write('</text>\n')
			elif sensor == 'CO2' :
				svg_file.write('<text style="text-anchor:end;" font-size="40px" x="450" y="655">')
				svg_file.write("%i" % (round(value)))
				svg_file.write('</text>\n')
				svg_file.write('<text style="text-anchor:start;" font-size="28px" x="458" y="644">')
				svg_file.write("ppm")
				svg_file.write('</text>\n')
				svg_file.write('<text style="text-anchor:start;" font-size="28px" x="482" y="667">')
				svg_file.write("CO")
				svg_file.write('</text>\n')
				svg_file.write('<text style="text-anchor:start;" font-size="20px" x="522" y="675">')
				svg_file.write("2")
				svg_file.write('</text>\n')
	elif module == outdoor :
		for sensor, value in moduleData.items() :
			if sensor == 'Temperature' :
				tempEntier=math.floor(value)
				tempDecimale=10*(value - tempEntier)
				svg_file.write('<text style="text-anchor:end;" font-size="100px" x="425" y="160">')
				svg_file.write("%i" % (tempEntier))
				svg_file.write('</text>\n')
				svg_file.write('<text style="text-anchor:start;" font-size="50px" x="420" y="155">,')
				svg_file.write("%i" % (tempDecimale))
				svg_file.write('</text>\n')
				svg_file.write('<circle cx="440" cy="90" r="7" stroke="black" stroke-width="3" fill="none"/>')
				svg_file.write('<text style="text-anchor:start;" font-size="35px" x="450" y="110">C</text>')
			elif sensor == 'Humidity' :
				svg_file.write('<text style="text-anchor:end;" font-size="30px" x="400" y="210">')
				svg_file.write("%i" % (round(value)))
				svg_file.write('%</text>\n')
	elif module == pluvio :
		for sensor, value in moduleData.items() :
			if sensor == 'sum_rain_24' :
				rain24 = value
			elif sensor == 'sum_rain_1' :
				rain1 = value

# Apparent Min/Max for today

svg_file.write('<text style="text-anchor:end;" font-size="35px" x="560" y="120">')
svg_file.write("%i" % (math.ceil(darkdata['daily']['data'][0]['apparentTemperatureMax'])))
svg_file.write('</text>\n')
svg_file.write('<circle cx="565" cy="98" r="4" stroke="black" stroke-width="3" fill="none"/>')
svg_file.write('<text style="text-anchor:start;" font-size="25px" x="570" y="110">C</text>')
svg_file.write('<text style="text-anchor:end;" font-size="35px" x="560" y="160">')

svg_file.write("%i" % (math.floor(darkdata['daily']['data'][0]['apparentTemperatureMin'])))
svg_file.write('</text>\n')
svg_file.write('<circle cx="565" cy="140" r="4" stroke="black" stroke-width="3" fill="none"/>')
svg_file.write('<text style="text-anchor:start;" font-size="25px" x="570" y="152">C</text>')

# Find min max for next days

minTemp=darkdata['daily']['data'][1]['apparentTemperatureMin']
maxTemp=darkdata['daily']['data'][1]['apparentTemperatureMax']
for i in range(2,4) :
	if darkdata['daily']['data'][i]['apparentTemperatureMin'] < minTemp : minTemp = darkdata['daily']['data'][i]['apparentTemperatureMin']
	if darkdata['daily']['data'][i]['apparentTemperatureMax'] > maxTemp : maxTemp = darkdata['daily']['data'][i]['apparentTemperatureMax']

pasTemp = (530-370)/(maxTemp-minTemp)

minPlace=360
maxPlace=560

n=305
for i in range(1,4) :
	jour = datetime.date.today() + datetime.timedelta(days=i) 
	svg_file.write('<text style="text-anchor:end;" font-size="35px" x="175" y="')
	svg_file.write("%i" % (n))
	svg_file.write('">')
	svg_file.write(jour.strftime("%A"))
	svg_file.write('</text>\n')
	
	tMin = (int)(355 + pasTemp*(darkdata['daily']['data'][i]['apparentTemperatureMin']-minTemp))
	svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
	svg_file.write("%i" % (tMin))
	svg_file.write('" y="')
	svg_file.write("%i" % (n))
	svg_file.write('">')
	svg_file.write("%i" % (math.floor(darkdata['daily']['data'][i]['apparentTemperatureMin'])))
	svg_file.write('</text>\n')
	svg_file.write('<circle cx="')
	svg_file.write("%i" % (tMin+5))
	svg_file.write('" cy="')
	svg_file.write("%i" % (n-20))
	svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
	svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
	svg_file.write("%i" % (tMin+10))
	svg_file.write('" y="')
	svg_file.write("%i" % (n-10))
	svg_file.write('">C</text>')

	tMax = (int)(400 + pasTemp*(darkdata['daily']['data'][i]['apparentTemperatureMax']-minTemp))
	svg_file.write('<text style="text-anchor:end;" font-size="35px" x="')
	svg_file.write("%i" % (tMax))
	svg_file.write('" y="')
	svg_file.write("%i" % (n))
	svg_file.write('">')
	svg_file.write("%i" % (math.ceil(darkdata['daily']['data'][i]['apparentTemperatureMax'])))
	svg_file.write('</text>\n')
	svg_file.write('<circle cx="')
	svg_file.write("%i" % (tMax+5))
	svg_file.write('" cy="')
	svg_file.write("%i" % (n-20))
	svg_file.write('" r="4" stroke="black" stroke-width="2" fill="none"/>')
	svg_file.write('<text style="text-anchor:start;" font-size="25px" x="')
	svg_file.write("%i" % (tMax+10))
	svg_file.write('" y="')
	svg_file.write("%i" % (n-10))
	svg_file.write('">C</text>')
	if (tMax-tMin > 50) :
		svg_file.write('<line x1="')
		svg_file.write("%i" % (tMin+50))
		svg_file.write('" x2="')
		space = tMax
		if darkdata['daily']['data'][i]['apparentTemperatureMax'] >= 10 : space -= 60 
		elif darkdata['daily']['data'][i]['apparentTemperatureMax'] >= 0 : space -= 40
		svg_file.write("%i" % (space)) # prendre en compte longueur des chiffres
		svg_file.write('" y1="')
		svg_file.write("%i" % (n-10))
		svg_file.write('" y2="')
		svg_file.write("%i" % (n-10))
		svg_file.write('" style="fill:none;stroke:black;stroke-linecap:round;stroke-width:10px;"/>')

	n += 90

svg_file.write('</g>\n')

# Add home icon
svg_file.write(geticon.getHome())

# add day icon
icon = darkdata['daily']['data'][0]['icon']
svg_file.write('<g transform="matrix(4,0,0,4,-35,-40)">')
if icon == 'clear-day' : svg_file.write(geticon.getClearDay())
elif icon == 'clear-night' : svg_file.write(geticon.getClearNight()) 
elif icon == 'rain' : svg_file.write(geticon.getRain()) 
elif icon == 'snow' : svg_file.write(geticon.getSnow()) 
elif icon == 'sleet' : svg_file.write(geticon.getSleet()) 
elif icon == 'wind' : svg_file.write(geticon.getWind()) 
elif icon == 'fog' : svg_file.write(geticon.getFog()) 
elif icon == 'cloudy' : svg_file.write(geticon.getCloudy()) 
elif icon == 'partly-cloudy-day' : svg_file.write(geticon.getPartlyCloudyDay())
elif icon == 'partly-cloudy-night' : svg_file.write(geticon.getPartlyCloudyNight())
svg_file.write('</g>\n')

# add next days icons
#  clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, or partly-cloudy-night
n=200
for i in range(1,4) :
	svg_file.write('<g transform="matrix(1.9,0,0,1.9,160,')
	svg_file.write("%i" % (n))
	svg_file.write(')">')
	
	icon = darkdata['daily']['data'][i]['icon']
	if icon == 'clear-day' : svg_file.write(geticon.getClearDay())
	elif icon == 'clear-night' : svg_file.write(geticon.getClearDay()) 
	elif icon == 'rain' : svg_file.write(geticon.getRain()) 
	elif icon == 'snow' : svg_file.write(geticon.getSnow()) 
	elif icon == 'sleet' : svg_file.write(geticon.getSleet()) 
	elif icon == 'wind' : svg_file.write(geticon.getWind()) 
	elif icon == 'fog' : svg_file.write(geticon.getFog()) 
	elif icon == 'cloudy' : svg_file.write(geticon.getCloudy()) 
	elif icon == 'partly-cloudy-day' : svg_file.write(geticon.getPartlyCloudyDay())
	elif icon == 'partly-cloudy-night' : svg_file.write(geticon.getPartlyCloudyDay())
	n += 90
	svg_file.write('</g>\n')

# Water bucket
svg_file.write('<path style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:6px;stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1" d="m 40,650 20,0 0,120 110,0 0,-120 20,0" />')
svg_file.write('<line x1="65" x2="75" y1="675" y2="675" style="fill:none;stroke:black;stroke-width:2px;"/>')
svg_file.write('<line x1="65" x2="75" y1="700" y2="700" style="fill:none;stroke:black;stroke-width:2px;"/>')
svg_file.write('<line x1="65" x2="75" y1="725" y2="725" style="fill:none;stroke:black;stroke-width:2px;"/>')
svg_file.write('<line x1="65" x2="75" y1="750" y2="750" style="fill:none;stroke:black;stroke-width:2px;"/>')

# Water drop
if rain24 == 0 :
	svg_file.write('<path d="m 133.92765,711.94362 c 0,10.47647 -8.76399,18.97912 -19.56247,18.97912 -10.79849,0 -19.762272,-8.50454 -19.562497,-18.97912 0.265462,-14.05037 11.020447,-19.77334 19.562497,-35.922 9.07296,15.61919 19.56247,25.44551 19.56247,35.922 z" stroke-miterlimit="4" style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:3;stroke-linecap:square;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dashoffset:0;stroke-opacity:1;marker-start:none;marker-mid:none;marker-end:none" />')
	svg_file.write('<line x1="85" x2="144" y1="730" y2="685" style="fill:none;stroke:black;stroke-width:4px;"/>')
else :
	rain24Entier=math.floor(rain24)
	rain24Decimale=10*(rain24 - rain24Entier)
	svg_file.write('<text style="text-anchor:end;" font-size="40px" x="128" y="720">')
	svg_file.write("%i" % (rain24Entier))
	svg_file.write('</text>')
	svg_file.write('<text style="text-anchor:start;" font-size="30px" x="128" y="720">,')
	svg_file.write("%i" % (rain24Decimale))
	svg_file.write('</text>')
	svg_file.write('<text style="text-anchor:start;" font-size="20px" x="78" y="756">')
	svg_file.write('mm/24h')
	svg_file.write('</text>')

if rain1 != 0 :
	rain1Entier=math.floor(rain1)
	rain1Decimale=10*(rain1 - rain1Entier)
	svg_file.write('<text style="text-anchor:end;" font-size="40px" x="170" y="185">')
	svg_file.write("%i" % (rain1Entier))
	svg_file.write('</text>')
	svg_file.write('<text style="text-anchor:start;" font-size="30px" x="170" y="185">,')
	svg_file.write("%i" % (rain1Decimale))
	svg_file.write('</text>')


# close file 
svg_file.write('</svg>')
svg_file.close()


