# Kindle-weather-station

Permet d’afficher la météo depuis une station Netatmo sur un Kindle. 

Le principe est le suivant :
  - Un ordinateur (raspberry par exemple) récupère toutes les 5 minutes les données de la Netatmo pour la météo courante et de forecast.io pour les prévision. Un script en python (createSVG.py) fabrique un SVG au format kindle (600x800 px).
  - Toujours sur l'ordinateur, le svg est transformé en fichier png avec un fond blanc avec Imagemagick
  - Le fichier est ensuite compressé et optimisé pour le kindle avec Pngcrush.
  - Puis, ce fichier est mis a disposition sur un serveur "web"
  - De son coté, le Kindle efface son écran avec "eips", récupère (avec wget) et affiche le png.

Le résultat d’un jour de pluie est visible ici :
https://raw.githubusercontent.com/iero/Kindle-weather-station/master/README.JPG

Ce processus est basé sur super travail de Matthew Petroff (http://mpetroff.net/2012/09/kindle-weather-display/) avec un affichage adapté aux données Netatmo et des unitées SI.

Pour cela, on utilise :
- Imagemagick - http://www.imagemagick.org/
- Forecast.io python library - https://github.com/ZeevG/python-forecast.io
- Pngcrush - http://pmt.sourceforge.net/pngcrush/
- Request python library - http://docs.python-requests.org/en/latest/
- Modified netatmo python api - https://github.com/philippelt/netatmo-api-python
- Les icones de Noah Blon - http://codepen.io/noahblon/details/lxukH

Vous avez donc besoin de vous authentifier au près de Netatmo et de foecast.io. Pour cela, il faut se connecter en temps que "dévelopeur". Pour notre usage de "particulier", c'est gratuit, et il faut se rendre ici :
  - Netatmo dev center : https://dev.netatmo.com/doc ('Create an app' en bas)
  - Forecast.io API : https://developer.forecast.io/ ('Register' en haut).

Vous obtiendrez des codes (api key) que vous rentrez dans le fichier settings.xml

Voici la procédure sur le raspberry (ou equivalent) :
- installer un serveur web (cf google)
- créer un répertoire kindle
- Compiler pngcrush (un binaire est gracieusement fourni)
- Copier les scripts du répertoire raspberry
- Modifier settings.xml pour mettre vos cpodes
- Modifier la derniere ligne de weather-script.sh pour copier le fichier sur le serveur web. 
- Ajouter dans le cron (crontab -e) la ligne :
*/5 * * * * /home/pi/kindle/weather-script.sh

Puis sur le Kindle :

- Jailbreaker le Kindle. Pour le Kindle 4, j’ai utilisé cette page : http://wiki.mobileread.com/wiki/Kindle4NTHacking
- Installer USBNetwork pour activer le ssh http://www.mobileread.com/forums/showthread.php?t=88004
- Installer Kual et activer le ssh via wifi http://www.mobileread.com/forums/showthread.php?t=203326

- Modifier kindle/display-weather pour mettre l’addresse du raspberry
- Mettre les fichiers du répertoire kindle dans /mnt/us/weather/
- Lancer le cron toutes les 5 minutes (décallées de 2 minutes) pour mettre à jour la page en entrant les commandes suivantes :

- kindle# /mnt/us/kindle/init-weather.sh
- kindle# mntroot rw
- kindle# echo "*/5+2 * * * * /mnt/us/weather/display-weather.sh" >> /etc/crontab/root
- kindle# mntroot ro
- kindle# /etc/init.d/cron restart
  
Pour faire la même chose sur un Kobo, Kevin explique la procédure ici : http://www.mobileread.com/forums/showthread.php?t=194376
