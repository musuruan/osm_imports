# coding=UTF-8

"""
ogr2osm translation rules for DBSN building data

Copyright (C) 2023 Andrea Musuruane <musuruan@gmail.com>

DBSN data distributed under the Open Data Commons Open Database License (ODbL) ver. 1.0

Data download available at:
https://www.igmi.org/it/dbsn-database-di-sintesi-nazionale

File list courtesy of Daniele Santini:
https://github.com/Danysan1/dbsn-import/blob/main/dbsn.tsv

More info at:
https://wiki.openstreetmap.org/wiki/Italy/DBSN

This script requires ogr2osm v1.0.0 or later:
https://github.com/roelderickx/ogr2osm

Open the GDB package with QGIS and save the buildings inside a municipality in a shapefile using:
https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorselection.html#select-by-location

After that run ogr2osm with:
ogr2osm -t edifici.py -f file.shp
"""

import ogr2osm

class Translate(ogr2osm.TranslationBase):
    def filter_tags(self, attrs):
        if not attrs:
            return

        tags = {}

        if attrs["edifc_nome"] != "UNK":
            tags["name"] = attrs["edifc_nome"]
        
        if attrs["edifc_sot"] == "02":
            tags["layer"] = "-1"

        match attrs["edifc_ty"]:
            case "05":
                tags["building"] = "house"
                tags["house"] = "terraced"
            case "11":
                tags["building"] = "church"
            case "22":
                tags["building"] = "church"
            case "23":
                 tags["building"] = "roof"
            case _:
                tags["building"] = "yes"

        match attrs["edifc_uso"]:
            case "0201":
                tags["amenity"] = "townhall"
            case "030102":
                tags["amenity"] = "hospital"
            case "0307":
                tags["amenity"] = "fire_station"
            case "0304":
                tags["amenity"] = "post_office"
            case "05":
                tags["amenity"] = "place_of_worship"
            case "100102":
                tags["amenity"] = "cinema"
            case "100101":
                tags["amenity"] = "library"
            
        match attrs["edifc_stat"]:
            case "01":
                if tags["building"] != "yes":
                    tags["construction"] = tags["building"]
                tags["building"] = "construction"
            case "02":
                tags["ruins"]="yes"
                
        return tags
        
    def filter_feature(self, ogrfeature, layer_fields, reproject):
        if not ogrfeature:
            return
        index = ogrfeature.GetFieldIndex('meta_ist')
        # Filter data from OSM
        if index >= 0 and ogrfeature.GetField(index) in ('03', '21', '23'):
            return None
        return ogrfeature
    
