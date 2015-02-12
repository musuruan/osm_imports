"""
csv2osm translation rules for Torino address data

Copyright (C) 2014-2015 Andrea Musuruane <musuruan@gmail.com>

The data are shipped in a file named "toponomastica_01062012.csv"
and they are available under the IODL 2.0 license at:
http://aperto.comune.torino.it/?q=node/260

Download csv2osm from:
https://github.com/OsmQc/mtl2osm/blob/master/mtl2osm/csv2osm.py

Convert with:
csv2osm.py toponomastica_01062012.csv toponomastica_01062012.osm --csv-dialect excel-semicolon --lon longitudine --lat latitudine --csv-encoding latin1 --translator torino.py -f

"""

import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    try:
        tags["addr:street"] = normalizer.translateName(attrs["Sedime"] + " " + attrs["Denominazione"])
    except KeyError:
        tags["fixme"] = "addr:street is missing"

    # Convert housenumber to lowercase
    tags["addr:housenumber"] = attrs["Numero_Radice"] + attrs["Secondario"].lower()

    tags["addr:postcode"] = attrs["Cap"]
    tags["addr:city"] = "Torino"

    return tags

