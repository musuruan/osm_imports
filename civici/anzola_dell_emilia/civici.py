"""
ogr2osm translation rules for Anzola dell'Emilia address data

Copyright (C) 2105 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip file named "T4_Shp.zip"
and they are availble under the CC0 license at:
http://dati.emilia-romagna.it/catalogodati/ricerca-avanzata/dato/102-102-04-civici-shp.html

Spatial Reference: Monte Mario / Italy zone 1 EPSG:3003

Run with:
ogr2osm.py -t civici.py -e 3003 -f Civici.shp
"""

import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    if "Etichett_1" in attrs:
        try:
            tags["addr:street"] = normalizer.translateName(attrs["Etichett_1"])
        except KeyError:
            tags["fixme"] = "addr:street is missing"
    if "Etichetta_" in attrs:
        # Convert housenumber to lowercase and remove slash
        tags["addr:housenumber"] = attrs["Etichetta_"].replace("/","").lower()

    tags["addr:postcode"] = "40011"
    tags["addr:city"] = "Anzola dell'Emilia"

    return tags
