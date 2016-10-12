# coding=UTF-8

"""
ogr2osm translation rules for Biella road data

Copyright (C) 2016 Andrea Musuruane <musuruan@gmail.com>

The data are availble under the CC-BY license at:
http://cartografia.provincia.biella.it/on-line/Home/articolo3007402.html

The data are shipped inside the zip file named "3016623Stradario.zip" 
and it is availble at:
http://cartografia.provincia.biella.it/on-line/Home/Repertorio/Consultazione/AT7Mobilitaetrasporti.html

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Run with:
ogr2osm.py --add-timestamp --add-version --positive-id -e 32632 -t stradario.py -f stradario08022016.shp
"""

def expandDUG(string):
    wordDict = {
        'Borg.a': 'Borgata',
        'C.ale': 'Casale',
        'C.na': 'Cascina',
        'C.rte': 'Corte',
        'C.so': 'Corso',
        'Camm.': 'Cammino',
        'Cant.': 'Cantone',
        'Casc.tto': 'Cascinotto',
        'Fraz.': 'Frazione',
        'G.ni': 'Giardini',
        'Gall.': 'Galleria',
        'Loc.': u'Località',
        'P.za': 'Piazza',
        'P.zale': 'Piazzale',
        'P.zetta': 'Piazzetta',
        'Pass.': 'Passeggiata',
        'Quart.re': 'Quartiere',
        'Reg.': 'Regione',
        'SP': 'Strada Provinciale',
        'Str.': 'Strada',
        'Svin.': 'Svincolo',
        'V.gio': 'Villaggio',
        'Vic.': 'Vicolo'}
    if string in wordDict.keys():
        return wordDict[string]
    else: 
        return string

def removeAbbreviations(name):
    name = name.replace("Avv." ,"Avvocato")
    name = name.replace("Btg." ,"Battaglione")
    name = name.replace("C.na" ,"Cascina")
    name = name.replace("Cap." ,"Capitano")
    name = name.replace("Cav." ,"Cavalier")
    name = name.replace("Cad.", "Caduti")
    name = name.replace("com.", "comunale")
    name = name.replace("Comm.", "Commendatore")
    name = name.replace("Dist.", "Distaccamento")
    name = name.replace("F.lli", "Fratelli")
    name = name.replace("Gr. Uff.", "Grand'ufficiale")
    name = name.replace("Inf.", "Inferiore")
    name = name.replace("inf.", "Inferiore")
    name = name.replace("Mons.", "Monsignor")
    name = name.replace("Sal.", "Salita")
    name = name.replace("Sen.", "Senatore")
    name = name.replace("Soc.", u"Società")
    name = name.replace("Sup.", "Superiore")
    name = name.replace("sup.", "Superiore")
    name = name.replace("Ten.", "Tenente")
    name = name.replace("Teol.", "Teologo")
    name = name.replace("vic." ,"vicinale")
    return name

def filterTags(attrs):
    if not attrs:
        return
    
    tags = {}
    
    if attrs["IMPORT"] == "0":
        # unclassified or residential
        tags["highway"] = "unclassified"
    elif attrs["IMPORT"] == "1":
        tags["highway"] = "secondary"
    elif attrs["IMPORT"] == "2":
        tags["highway"] = "primary"
    elif attrs["IMPORT"] == "9":
        tags["highway"] = "tertiary"

    if attrs["SENSO"] == "0":
        tags["highway"] = "footway"
    elif attrs["SENSO"] == "2":
        tags["oneway"] = "yes"
        
    if attrs["TERRA"] == "1":
        tags["surface"] = "asphalt"
    elif attrs["TERRA"] == "2":
        tags["highway"] = "track"
        tags["surface"] = "unpaved"
    elif attrs["TERRA"] == "3":
        tags["highway"] = "path"
    elif attrs["TERRA"] == "4":
        tags["surface"] = "cobblestone"
    elif attrs["TERRA"] == "5":
        tags["highway"] = "steps"
    elif attrs["TERRA"] == "6":
        tags["surface"] = "paving_stones"
    elif attrs["TERRA"] == "7":
        tags["surface"] = "sett" 
    
    if attrs["CIELO"] == "4":
        tags["tunnel"] = "yes"
        tags["layer"] = "-1"
        
    if attrs["LIMIT"] == "1":
        tags["motor_vehicle"] = "no"
    elif attrs["LIMIT"] == "2" or attrs["LIMIT"] == "3":
        tags["motor_vehicle:conditional"] = "destination"
        tags["fixme"] = "Specificare ZTL"
    elif attrs["LIMIT"] == "9":
        tags["access"] = "no"
    elif attrs["LIMIT"] == "10":
        tags["maxweight"] = "2"
    elif attrs["LIMIT"] == "11":
        tags["maxweight"] = "7"
    
    tags["is_in"] = attrs["Nome_Com_1"]

    if attrs["TOPO_PROV"] not in ("", "0", "_001", "_002", "_003"):
        tags["ref"] = attrs["TOPO_PROV"].upper().strip()
        tags["ref"] = tags["ref"].replace("SP ", "SP")
        tags["ref"] = tags["ref"].replace("NSA ", "NSA")
    
    if attrs["Toponimo"] != "":
        if attrs["TOPO_PROV"] != attrs["Toponimo"]:
            firstSpace = attrs["Toponimo"].find(' ')
            
            DUG = attrs["Toponimo"][:firstSpace].strip()
            DUG = expandDUG(DUG)
            
            denominazione = attrs["Toponimo"][firstSpace+1:].strip()
            denominazione = denominazione.replace("' ", "'")
            denominazione = removeAbbreviations(denominazione)
            
            tags["name"] = DUG + " " + denominazione
            
            if DUG == "Rotonda":
                tags["junction"] = "roundabout"
            
            if DUG == "Svincolo" or DUG == "Rotonda":
                    del tags["name"]

    return tags

def filterFeature(ogrfeature, fieldNames, reproject):
    if not ogrfeature:
        return

    # COD_CAT == Z100 means feature is outside the Province of Biella
    index = ogrfeature.GetFieldIndex('COD_CAT')
    if index >= 0 and ogrfeature.GetField(index) == "Z100":
        return None

    return ogrfeature
    
