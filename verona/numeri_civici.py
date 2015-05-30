"""
ogr2osm translation rules for Verona address data

Copyright (C) 2015 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip file named 
"SHP_NUMERAZIONE_CIVICA_point 26-02-21014.zip" 
and they are availble under the IODL 2.0 license at:
http://www.comune.verona.it/nqcontent.cfm?a_id=41435

Spatial Reference: EPSG:26591 (Gauss-Boaga/Roma40 fuso OVEST)

Run with:
ogr2osm.py -e 26591 -t numeri_civici.py -f NUMERAZIONE_CIVICA_point.shp
"""

import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}
    tags["addr:street"] = normalizer.translateName(attrs["NOME_VIA"])
    tags["addr:housenumber"] = attrs["NUM_CIV"][0:attrs["NUM_CIV"].find(".")] + attrs["ESP"].lower()
    if attrs["CAP"] != "":
        tags["addr:postcode"] = attrs["CAP"]
    else:
        tags["fixme"] = "addr:postcode is missing"
    tags["addr:city"] = "Verona"
    return tags

