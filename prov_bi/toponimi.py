# coding=UTF-8

"""
ogr2osm translation rules for Biella address data

Copyright (C) 2016 Andrea Musuruane <musuruan@gmail.com>

The data are availble under the CC-BY license at:
http://cartografia.provincia.biella.it/on-line/Home/articolo3007402.html

The data are shipped inside the zip file named "3026619toponimi150714.zip" 
and they are availble at:
http://cartografia.provincia.biella.it/on-line/Home/Repertorio/Consultazione/articolo3000189.html

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Run with:
ogr2osm.py -e 32632 -t toponimi.py -f toponimi150714.shp
"""

def fixPlaceName(name):
    name = name.replace("Cavaglia'", u"Cavaglià")
    name = name.replace("BIELLA", "Biella")
    return name

def removeAbbreviations(name):
    name = name.replace("Fraz. ", "Frazione ")
    name = name.replace("Cant. ", "Cantone ")
    name = name.replace("C.le ", "Colle ")
    name = name.replace("C.ale ", "Casale ")
    name = name.replace("L. ", "Lago ")
    name = name.replace("Loc. ", u"Località ")
    name = name.replace("Borg.a ", "Borgata ")
    name = name.replace("Rif. ", "Rifugio ")
    name = name.replace("Reg. ", "Regione ")
    name = name.replace("C. ", "Cascina ")
    name = name.replace("Casc. ", "Cascina ")
    name = name.replace("C.na ", "Cascina ")
    name = name.replace("C.ne ", "Cascine ")
    name = name.replace("Inf.", "Inferiore")
    name = name.replace("Sup.", "Superiore")
    return name

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    tags["name"] = removeAbbreviations(attrs["Label"])
    firstWord = tags["name"][: tags["name"].find(' ')]

    if attrs["Label_1"] != "":
        tags["alt_name"] = removeAbbreviations(attrs["Label_1"])

    classifica = attrs["Classifica"]

    if classifica == "Cascina":
        tags["place"] = "farm"
    elif classifica == "Cime e monti":
        tags["natural"] = "peak"
    elif classifica == "Lago":
        tags["natural"] = "water"
        tags["water"] = "lake"
    elif classifica == u"Località":
        # Solo Frazioni e Borgate
        tags["place"] = "hamlet"
        tags["name"] = tags["name"].replace(firstWord + " ", "")
    elif classifica == "Rifugio":
        if firstWord in ("Capanna", "Rifugio"):
            tags["tourism"] = "alpine_hut"
        else:
            tags["tourism"] = "wilderness_hut"

    if attrs["COMUNE_TOP"] != "":
        tags["is_in"] = fixPlaceName(attrs["COMUNE_TOP"])

    return tags

def filterFeature(ogrfeature, fieldNames, reproject):
    if not ogrfeature:
        return

    index = ogrfeature.GetFieldIndex('Classifica')
    if index >= 0 and ogrfeature.GetField(index) in ("Alpeggio", "Castello", "Cave", "Cimitero", "Edificio", "Luogo di culto", "Monastero", "Passi e bocchette", "Ponte", "Villa"):
        return None

    if index >= 0 and ogrfeature.GetField(index) == "Località":
        labelIndex = ogrfeature.GetFieldIndex('Label')
        label = ogrfeature.GetField(labelIndex)
        firstWord = label[: label.find(' ')]
        if firstWord not in ("Fraz.", "Borg.a"):
            return None

    return ogrfeature

