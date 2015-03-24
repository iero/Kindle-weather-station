#!/bin/sh

cd "$(dirname "$0")"

python createSVG.py
convert -background white kindleStation.svg kindleStation.png
/home/pi/kindle/pngcrush -s -c 0 -ow kindleStation.png
cp -f kindleStation.png /home/pi/domoticz/www/kindle/weather-script-output.png
