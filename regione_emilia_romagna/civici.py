"""
ogr2osm translation rules for Emilia-Romagna address data

Copyright (C) 2106 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip files, one for each province, and they are 
availble under the CC-BY 2.5 license at:
http://geoportale.regione.emilia-romagna.it/it/download/dati-e-prodotti-cartografici-preconfezionati/database-topografico/gestione-viabilita-e-indirizzi/dati-preconfezionati-dbtr-civico-ncv_gpt

Spatial Reference: ESTR89 UTM Zona 32N (EPSG:25832)

Run with:
ogr2osm.py -t civici.py -e 25832 -f V_NCV_GPT.shp
"""

import string
import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}
    
    tags["addr:housenumber"] = attrs["NM_CIV"] + attrs["SB_CIV"].lower()
    tags["addr:street"] = normalizer.translateName(attrs["TP_NOM"])
    tags["addr:city"] = string.capwords(attrs["NOME_C"])

    return tags

