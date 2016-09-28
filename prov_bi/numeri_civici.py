# coding=UTF-8

"""
ogr2osm translation rules for Biella address data

Copyright (C) 2016 Andrea Musuruane <musuruan@gmail.com>

The data are availble under the CC-BY license at:
http://cartografia.provincia.biella.it/on-line/Home/articolo3007402.html

The data are shipped inside the zip file named "3027997Numeri_civici.zip" 
and they are availble at:
http://cartografia.provincia.biella.it/on-line/Home/Repertorio/Consultazione/AT7Mobilitaetrasporti.html

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Run with:
ogr2osm.py -e 32632 -t numeri_civici.py -f Numeri_civici08022016.shp
"""

def expandDUG(string):
    wordDict = {
        'Borg.a': 'Borgata',
        'C.ale': 'Casale',
        'C.na': 'Cascina',
        'C.rte': 'Corte',
        'C.so': 'Corso',
        'Cant.': 'Cantone',
        'Casc.tto': 'Cascinotto',
        'Fraz.': 'Frazione',
        'Gall.': 'Galleria',
        'Loc.': u'Località',
        'P.za': 'Piazza',
        'P.zale': 'Piazzale',
        'P.zetta': 'Piazzetta',
        'Quart.re': 'Quartiere',
        'Reg.': 'Regione',
        'SP': 'Strada Provinciale',
        'Str.': 'Strada',
        'V.gio': 'Villaggio',
        'Vic.': 'Vicolo'}
    if string in wordDict.keys():
        return wordDict[string]
    else: 
        return string

def removeAbbreviations(name):
    name = name.replace("Avv." ,"Avvocato")
    name = name.replace("C.na" ,"Cascina")
    name = name.replace("Cav." ,"Cavalier")
    name = name.replace("Cad.", "Caduti")
    name = name.replace("Inf.", "Inferiore")
    name = name.replace("Soc.", u"Società")
    name = name.replace("Sup.", "Superiore")
    name = name.replace("vic." ,"vicinale")
    return name

def filterTags(attrs):
    if not attrs:
        return

    tags = {}
    
    # Convert housenumber to lowercase
    tags["addr:housenumber"] = attrs["NUMERO"].lower()
    
    if attrs["Toponimo"] != "":
        firstSpace = attrs["Toponimo"].find(' ')
        
        DUG = attrs["Toponimo"][:firstSpace].strip()
        DUG = expandDUG(DUG)
        
        denominazione = attrs["Toponimo"][firstSpace+1:].strip()
        denominazione = denominazione.replace("' ", "'")
        denominazione = removeAbbreviations(denominazione)
        
        tags["addr:street"] = DUG + " " + denominazione
        # tags["addr:postcode"] is missing
        tags["addr:city"] = attrs["Nome_Comun"]
    else:
        tags["fixme"] = "addr:street and addr:city are missing"
    
    return tags

def filterFeature(ogrfeature, fieldNames, reproject):
    if not ogrfeature:
        return
    
    # Filter addresses with NUMERO=sn
    index = ogrfeature.GetFieldIndex('NUMERO')
    if index >= 0 and ogrfeature.GetField(index) == "sn":
        return None
    
    return ogrfeature
