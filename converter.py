#! usr/bin/env python
from geopy.geocoders import Nominatim
from geopy import geocoders
from sys import argv
from os.path import exists
import simplejson as json
import time

script, out_file = argv

dataJson = json.load(open("Caracteristiques+Lieux2011-2015.json"))
dataFinal = []

nbPasAjoute=0

#geolocator = Nominatim() #Open Sreet Map
geolocator = geocoders.GoogleV3(api_key='XXX') # Google Map

for d in dataJson:
    if d["long"]!=None or d["adr"] != None:  # Si les coordonnées gps et adresse sont présente
        aAjouter = True
        if d["long"]==None and d["adr"] != None: #Si l'adresse est présente mais pas les coordonnées gps
            #mise en forme de l'adresse pour passer de "1, TOMBLAINE (RUE DE)" à "1, RUE DE TOMBLAINE"
            d["adr"] = d["adr"].replace(' )', '')
            d["adr"] = d["adr"].replace(')', '')
            d["adr"] = d["adr"].replace('( ', '(')

            #Ajout de la ville
            departement = int(d["dep"]/10)
            codeVille = str(departement) + str(d["com"])

            if codeVille == "54025":
                ville = "Art-sur-Meurthe"
            elif codeVille == "54184":
                ville = "ESSEY-LÈS-NANCY"
            elif codeVille == "54257":
                ville = "HEILLECOURT "
            elif codeVille == "54274":
                ville = "JARVILLE-LA-MALGRANGE"
            elif codeVille == "54304":
                ville = "LAXOU"
            elif codeVille == "54339":
                ville = "MALZÉVILLE"
            elif codeVille == "54395":
                ville = "NANCY"
            elif codeVille == "54482":
                ville = "SAINT-MAX"
            elif codeVille == "54498":
                ville = "SEICHAMPS"
            elif codeVille == "54547":
                ville = "VANDŒUVRE-LÈS-NANCY"
            elif codeVille == "54165":
                ville = "DOMMARTEMONT"
            elif codeVille == "54197":
                ville = "FLÉVILLE-DEVANT-NANCY"
            elif codeVille == "54265":
                ville = "HOUDEMONT"
            elif codeVille == "54300":
                ville = "LANEUVEVILLE-DEVANT-NANCY"
            elif codeVille == "54328":
                ville = "LUDRES"
            elif codeVille == "54339":
                ville = "MAXÉVILLE"
            elif codeVille == "54439":
                ville = "PULNOY"
            elif codeVille == "54495":
                ville = "SAULXURES-LÈS-NANCY"
            elif codeVille == "54526":
                ville = "TOMBLAINE"
            elif codeVille == "54578":
                ville = "VILLERS-LÈS-NANCY"


            try: #si numéro de rue dans l'adresse
                tmpAdr = d["adr"].split(",") #sépare le numéro et le nom de la rue
                tmpAdr2 = tmpAdr[1].split("(")
                adresse = tmpAdr[0] + " " + tmpAdr2[1] + tmpAdr2[0] + " " + ville
            except: #sinon
                try:
                    tmpAdr2 = d["adr"].split("(")
                    adresse = tmpAdr2[1] + tmpAdr2[0] + " " + ville
                except: #s'il n'y a pas de parenthèse (l'adresse est déjà bien remplie)
                    adresse = d["adr"] + " " + ville

            print(adresse)
            #transformation adresse en coordonnées
            infoLoc = geolocator.geocode(adresse, timeout=10) #une seul requête pour éviter de se faire bannir
            try:
                if infoLoc.longitude!=None:
                    d["long"] = infoLoc.longitude
                    d["lat"] = infoLoc.latitude
            except:
                aAjouter = False
                nbPasAjoute=nbPasAjoute+1

            time.sleep(1) #Les règles d'open street map imposent au max 1 requête/s

        if aAjouter == True:
            dataFinal.append(d) #permet de retirer les accidents où on a ni gps ni adresse
    else:
        nbPasAjoute = nbPasAjoute + 1

geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [d["long"], d["lat"]],
            },
        "properties" : d,
     } for d in dataFinal]
}

output = open(out_file, 'w')
json.dump(geojson, output)

print (geojson)
print("Nombre d'accidents pas ajouté : " + str(nbPasAjoute))
