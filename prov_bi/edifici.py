# coding=UTF-8

"""
ogr2osm translation rules for Biella address data

Copyright (C) 2016 Andrea Musuruane <musuruan@gmail.com>

The data are availble under the CC-BY license at:
http://cartografia.provincia.biella.it/on-line/Home/articolo3007402.html

The data are shipped inside the zip file named "3020502Edifici.zip" 
and they are availble at:
http://cartografia.provincia.biella.it/on-line/Home/Repertorio/Consultazione/AT7Mobilitaetrasporti.html

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Run with:
ogr2osm.py -e 32632 -t edifici.py -f edifici08022016.shp
"""

def removeAbbreviations(name):
    name = name.replace("Bas.ca", "Basilica")
    name = name.replace("Cap.la", "Cappella")
    name = name.replace("C.na", "Cascina")
    name = name.replace("Casc.tto", "Cascinotto")
    name = name.replace("Catt.le", "Cattedrale")
    name = name.replace("Ch.etta", "Chiesetta")
    name = name.replace("Conv.to", "Convento")
    name = name.replace("Inf.", "Inferiore")
    name = name.replace("Ist.", "Istituto")
    name = name.replace("I.T.I.S.", "Istituto Tecnico Industriale Statale")
    name = name.replace("Monast.o", "Monastero")
    name = name.replace("Orat.o", "Oratorio")
    name = name.replace("Pal.zo", "Palazzo")
    name = name.replace("Parr.le", "parrocchiale")
    name = name.replace("Profes.", "Professionale")
    name = name.replace("Rif.", "Rifugio")
    name = name.replace("Sant.o", "Santuario")
    name = name.replace("Staz.", "Stazione")
    name = name.replace("Sup.", "Superiore")
    name = name.replace("Tecn.", "Tecnico")
    name = name.replace("Ten.", "Tenuta")
    name = name.replace("Uff.", "Ufficio")
    return name
    
def filterTags(attrs):
    if not attrs:
        return

    tags = {}
    
    buildingDict = {
        'Alpe': 'farm',
        'Basilica': 'church',
        'Cappella': 'chapel',
        'Casa': 'house',
        'Cascina': 'farm',
        'Cascinotto': 'farm',
        'Case': 'yes',
        'Cattedrale': 'cathedral',
        'Chiesa': 'church',
        'Chiesa Parr.': 'church',
        'Chiesetta': 'chapel',
        'Commenda': 'yes',
        'Condominio': 'apartments',
        'Convento': 'yes',
        'Monastero': 'yes',
        'Moschea': 'mosque',
        'Oratorio': 'church',
        'Palazzo': 'yes',
        'Sala del Regno': 'yes',
        'Santuario': 'church',
        'Tenuta': 'farm',
        'Villa': 'yes'}

    if attrs["Pref_Edifi"] in buildingDict.keys():
        tags["building"] = buildingDict[attrs["Pref_Edifi"]]
    else: 
        tags["building"] = "yes"
        
    if tags["building"] in ("church", "cathedral", "chapel"):
        tags["amenity"] = "place_of_worship"
        tags["religion"] = "christian"
        tags["denomination"] = "catholic"
        
    if tags["building"] == "mosque":
        tags["amenity"] = "place_of_worship"
        tags["religion"] = "muslim"
        
    if "Edifici" in attrs and attrs["Edifici"] != "":
        tags["name"] = removeAbbreviations(attrs["Edifici"]).strip()
        
        if tags["name"] == "Sala del Regno":
            tags["amenity"] = "place_of_worship"
            tags["religion"] = "christian"
            tags["denomination"] = "jehovahs_witness"
        
        if tags["name"] == "Carabinieri":
            tags["amenity"] = "police"
            tags["operator"] = "Carabinieri"
            
        if tags["name"] == "Questura":
            tags["amenity"] = "police"
            tags["operator"] = "Polizia di Stato"
            
        if tags["name"] == "Polizia Stradale":
            tags["amenity"] = "police"
            tags["operator"] = "Polizia di Stato"
            
        if tags["name"] == "Polizia Municipale":
            tags["amenity"] = "police"
            tags["operator"] = "Polizia Municipale"
            
        if tags["name"] == "Guardia di Finanza":
            tags["amenity"] = "police"
            tags["operator"] = "Guardia di Finanza"
            
        if tags["name"] == "Ecocentro":
            tags["amenity"] = "recycling"
            tags["recycling_type"] = "centre"
        
        if tags["name"] == "Municipio":
            tags["building"] = "civic"
            tags["amenity"] = "townhall"
            
        if tags["name"] == "Prefettura":
            tags["building"] = "public"
            tags["office"] = "government"
            
        if tags["name"] == "Torre campanaria":
            tags["man_made"] = "tower"
            tags["tower:type"] = "bell_tower"
       
        if tags["name"].startswith("Ufficio Postale"):
            tags["amenity"] = "post_office"
            
        if tags["name"].startswith("Casa di Riposo"):
            tags["amenity"] = "social_facility"
            tags["social_facility"] = "assisted_living"
            tags["social_facility:for"] = "senior"
            
        if tags["name"].startswith("Palazzetto dello Sport"):
            tags["leisure"] = "sports_centre"
            
        if tags["name"].startswith("Scuola Materna"):
            tags["amenity"] = "kindergarten"
            
        if tags["name"].startswith("Stazione Ferroviaria"):
            tags["building"] = "train_station"
            
        if tags["name"].startswith("Casa di cura") or tags["name"] == "Ospedale" or  tags["name"] == "Nuovo Ospedale":
            tags["building"] = "hospital"
            
        if tags["name"].startswith("Vigili del Fuoco"):
            tags["building"] = "fire_station"
        
        firstWord = tags["name"][:tags["name"].find(" ")]

        if firstWord == "Biblioteca":
            tags["amenity"] = "library"
            
        if firstWord == "Bocciodromo":
            tags["leisure"] = "sports_centre"
            tags["sport"] = "boules"
            tags["type"] = "lyonnaise"
        
        if firstWord == "Castello":
            tags["historic"] = "castle"
            
        if firstWord in ("Cinema", "Cineteatro"):
            tags["amenity"] = "cinema"
            tags["building"] = "cinema"
            
        if firstWord == "Cimitero":
            tags["tomb"] = "columbarium"
            
        if firstWord == "Diga":
            tags["waterway"] = "dam"
            
        if firstWord in ("Ecomuseo", "Museo"):
            tags["amenity"] = "museum"
            
        if firstWord == "Farmacia":
            tags["amenity"] = "pharmacy"
            tags["dispensing"] = "yes"
            
        if firstWord == "Palestra":
            tags["leisure"] = "sports_centre"
            
        if firstWord in ("Scuola", "Istituto"):
            tags["building"] = "school"
            
        if firstWord == "Teatro":
            tags["amenity"] = "theatre"
            
        if firstWord == u"Università":
            tags["building"] = "university"
            tags["amenity"] = "university"
            
        if firstWord == "Alpe" or firstWord == "Cascina" or firstWord == "Cascinotto" or firstWord == "Tenuta" or firstWord == "Discarica" or firstWord == "Cimitero" or tags["name"].startswith("Stazione Ferroviaria"):
            del tags["name"]
        
    return tags
