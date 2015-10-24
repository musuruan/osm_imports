"""
ogr2osm translation rules for Modena address data

Copyright (C) 2105 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip file named "civici.zip"
and they are availble under the CC0 license at:
http://dati.emilia-romagna.it/catalogodati/ricerca-avanzata/dato/100809-100809-numerazione-civica-del-territorio-comunale.html

Spatial Reference: Gauss Boaga Fuso Ovest EPSG:26591

Run with:
ogr2osm.py -t civici.py -e 26591 -f civici.shp
"""

import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    tags["addr:housenumber"] = attrs["NCIVSUB"]
    tags["addr:street"] = normalizer.translateName(attrs["DENOMINAZI"])
    if attrs["CAP"] != "":
        tags["addr:postcode"] = attrs["CAP"]
    else:
        tags["fixme"] = "addr:postcode is missing"
    tags["addr:city"] = "Modena"

    return tags

