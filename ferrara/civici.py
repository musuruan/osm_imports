"""
ogr2osm translation rules for Ferrara address data

Copyright (C) 2105 Andrea Musuruane <musuruan@gmail.com>

The data are shipped inside the zip file named "civici.zip"
and they are availble under the IODL 2.0 license at:
http://www.comune.fe.it/index.phtml?id=3513

Spatial Reference: Gauss Boaga Fuso Ovest EPSG:26591

Run with:
ogr2osm.py -t civici.py -e 26591 -f Civici.shp
"""

import normalizer

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    tags["addr:housenumber"] = attrs["NUMERO"] + attrs["ESPONENTE"].lower()
    tags["addr:street"] = normalizer.translateName(attrs["VIA_NOME_U"])
    tags["addr:city"] = "Ferrara"

    return tags

