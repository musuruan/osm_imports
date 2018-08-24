#!/usr/bin/python3

import csv
from fuzzywuzzy import process

tipoVia = {}
fTipoVia = open("TIPOVIA.csv", "r")
csvTipoVia = csv.DictReader(fTipoVia, delimiter = ",")
for tipo in csvTipoVia:
    tipoVia[tipo["CODICE"]] = tipo["DESC_ESTESA"].upper()
fTipoVia.close()

fOD = open("Viario_20180718.csv", "r")
csvOD = csv.DictReader(fOD, delimiter = ";")

fMerge = open("Viario_OSM_20180718.csv", "w")
csvMergeFields = ["CODICE_VIA", "STATO", "TIPO", "DENOMINAZIONE", "DATA_INTITOLAZIONE", "ANNO_SOPPRESSIONE", "DESCRITTIVO", "ANNCSU", "OPENSTREETMAP", "PROGANNCSU", "TOPONIMO_OSM", "RATIO"]
csvMerge = csv.DictWriter(fMerge, delimiter = ";", fieldnames=csvMergeFields)
csvMerge.writeheader()

for stradaOD in csvOD:
    nomiStradeOSM = []
    
    fOSM = open("Stradario_OSM_20180810.csv", "r")
    csvOSM = csv.DictReader(fOSM, delimiter = ";")
    for stradaOSM in csvOSM:
        if stradaOSM["loc_ref"] == stradaOD["CODICE_VIA"]:
            nomiStradeOSM.append(stradaOSM["name"])
    fOSM.close()
           
    nomeOD = tipoVia[stradaOD["TIPO"]] + " " + stradaOD["DESCRITTIVO"]
    if nomiStradeOSM != []:
        nomeOSM, ratio = process.extractOne(nomeOD, nomiStradeOSM)
    else:
        nomeOSM = ""

    stradaOD["TOPONIMO_OSM"] = nomeOSM
    stradaOD["RATIO"] = ratio
    csvMerge.writerow(stradaOD)

fOD.close()
fMerge.close()
