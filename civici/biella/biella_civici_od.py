"""
ogr2osm translation rules for Biella address data

Copyright (C) 2014 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip file named "biella_civici_od.zip" 
and they are availble under the IODL 2.0 license at:
http://www.comune.biella.it/sito/index.php?biella-open-data

The file "elenco_viesit.csv" must have been preprocessed to append a 
column with street names normalized to follow Italian OSM naming 
conventions
"""

import csv

streetNames = {}

# Read toponyms
inputFile = open("elenco_viesit_osm.csv", "rb")
streetReader = csv.DictReader(inputFile, delimiter=";")

for row in streetReader:
    streetNames[row["Id_VIA"]] = row["NOME_VIA_OSM"].decode("utf-8")

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    if "ID_VIA" in attrs:
        try:
            tags["addr:street"] = streetNames[attrs["ID_VIA"]]
        except KeyError:
            tags["fixme"] = "addr:street is missing"
    if "CIVICO" in attrs:
    # Convert housenumber to lowercase
        tags["addr:housenumber"] = attrs["CIVICO"].lower()

    tags["addr:postcode"] = "13900"
    tags["addr:city"] = "Biella"

    return tags

