# coding=UTF-8

"""
ogr2osm translation rules for Milan address data

Copyright (C) 2018 Andrea Musuruane <musuruan@gmail.com>

The data are available under the CC-BY-2.5-IT license at:
https://geoportale.comune.milano.it/ATOM/SIT/Toponomastica/NumeriCivici_Service.xml

The waiver for inclusion in OSM is available at:
https://geoportale.comune.milano.it/sit/toponomastica/

Please read import wiki page for further info:
https://wiki.openstreetmap.org/wiki/Import/Catalogue/Address_import_for_Milan

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Run with:
ogr2osm.py -e 32632 -t civici.py -f Civici_20180718.shp
"""

import csv

nomiStradeOSM = {}
fOSM = open("Viario_OSM_20180718.csv", "r")
csvOSM = csv.DictReader(fOSM, delimiter = ";")
for stradaOSM in csvOSM:
        nomiStradeOSM[stradaOSM["CODICE_VIA"]] = stradaOSM["TOPONIMO_OSM"]
fOSM.close()

def filterTags(attrs):
    if not attrs:
        return

    tags = {}
    
    tags["loc_ref"] = attrs["IDMASTER"]
    tags["addr:housenumber"] = attrs["NUMEROCOMP"].lower()
    tags["addr:city"] = "Milano"
    
    nomeStrada = nomiStradeOSM[attrs["CODICE_VIA"]]
    if nomeStrada != "":
        tags["addr:street"] = unicode(nomeStrada, "utf-8")
    else:
        tags["fixme"] = "addr:street is missing"
    
    return tags

def filterFeature(ogrfeature, fieldNames, reproject):
    if not ogrfeature:
        return
        
    # Filtra civici soppressi
    index = ogrfeature.GetFieldIndex('STATOCIVICO')
    if index >= 0 and ogrfeature.GetField(index) == "99":
        return None
    
    return ogrfeature
