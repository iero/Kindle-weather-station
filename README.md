# Kindle-weather-station

Permet d’afficher la météo depuis une station Netatmo sur un Kindle.

Basé sur le travail de Matthew Petroff (http://mpetroff.net/2012/09/kindle-weather-display/) mais adapté et francisé.

Utilise :
- Forecast.io python library - https://github.com/ZeevG/python-forecast.io
- Pngcrush - http://pmt.sourceforge.net/pngcrush/
- Request python library - http://docs.python-requests.org/en/latest/
- Modified netatmo python api - https://github.com/philippelt/netatmo-api-python

Vous avez donc besoin d’une API Netatmo et d’une API foecast.io

Sur le raspberry (ou equivalent) :
- créer un répertoire kindle
- Compiler pngcrush - http://pmt.sourceforge.net/pngcrush/
- Copier les scripts du répertoire raspberry
- Modifier settings.xml

Sur le Kindle (de mémoire, j’ai oublié le pass root)

- Jailbreaker le Kindle. Pour le Kindle 4, j’ai utilisé cette page : http://wiki.mobileread.com/wiki/Kindle4NTHacking
- Installer USBNetwork pour activer le ssh http://www.mobileread.com/forums/showthread.php?t=88004
- Installer Kual et activer le ssh via wifi http://www.mobileread.com/forums/showthread.php?t=203326

- Modifier kindle/display-weather pour mettre l’addresse du raspberry
- Mettre les fichiers du répertoire kindle sur le Kindle
- Lancer le cron toutes les 5 minutes (décallées de 2 minutes) pour mettre à jour la page

kindle# /mnt/us/kindle/init-weather.sh
kindle# mntroot rw
kindle# echo « */5+2 * * * * /mnt/us/kindle/display-weather.sh >> /etc/crontab/root
kindle# mntroot ro
kindle# /etc/init.d/cron restart