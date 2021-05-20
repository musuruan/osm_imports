# coding=UTF-8

"""
ogr2osm translation rules for Montagna in Valtellina address data

Copyright (C) 2021 Andrea Musuruane <musuruan@gmail.com>

The data are availble under the CC-BY 4.0 license with an ODbL addendum:
https://wikimediaitalia.nws.netways.de/index.php/s/yNDToN8tgzaX4QT

Spatial Reference: EPSG:32632 (WGS 84 / UTM zone 32N)

Requires ogr2osm v1.0.0:
https://github.com/roelderickx/ogr2osm

Run with:
ogr2osm -e 32632 -t civici.py -f Civici_OSM.shp
"""

import ogr2osm

class TranslateCivici(ogr2osm.TranslationBase):

    def filter_tags(self, attrs):
        if not attrs:
            return

        tags = {}

        tags["addr:housenumber"] = attrs["CIVICO"].lower()
        tags["addr:street"] = attrs["NOME_VIA"]
        tags["addr:postcode"] = "23020"
        tags["addr:city"] = "Montagna in Valtellina"

        return tags

