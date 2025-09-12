# coding=UTF-8

"""
ogr2osm translation rules for DBSN building data

Copyright (C) 2023-2025 Andrea Musuruane <musuruan@gmail.com>

The data are available under the ODbL license at:
https://www.igmi.org/it/dbsn-database-di-sintesi-nazionale

File list courtesy of Daniele Santini:
https://github.com/Danysan1/dbsn-import/blob/main/dbsn.tsv

Requires ogr2osm v1.0.0:
https://github.com/roelderickx/ogr2osm

Run with:
ogr2osm -t strade.py -f Vercelli_dbsn.gdb -o strade_VC.osm
"""

import ogr2osm
import string
from osgeo import ogr

class Translate(ogr2osm.TranslationBase):

    def filter_layer(self, layer):
        if layer.GetName() != ('tr_str'):
            return None
        else:
            return layer


    def filter_feature(self, ogrfeature, layer_fields, reproject):
        if not ogrfeature:
            return

        # Filter data from OSM
        index = ogrfeature.GetFieldIndex('meta_ist')
        if index >= 0 and ogrfeature.GetField(index) in ('03', '21', '23'):
            return None

        return ogrfeature


    def filter_tags(self, attrs):
        if not attrs:
            return

        tags = {}

        # Ho trovato solo nomi di autostrade e strade provinciali
        if attrs["tr_str_nom"].upper() != "UNK":
            tags["name"] = attrs["tr_str_nom"]

        match attrs["tr_str_cf"]:
            case "01":
                tags["highway"] = "motorway"
            case "02":
                tags["highway"] = "trunk"
            case "03":
                tags["highway"] = "road" # Può essere primary, secondary o tertiary
            case "04":
                tags["highway"] = "road" # Può essere primary, secondary o tertiary
            case "05":
                tags["highway"] = "residential"
            case "06":
                tags["highway"] = "unclassified" # Può essere anche una track

        if attrs["tr_str_liv"] == "01":
            tags["tunnel"] = "yes"
            tags["layer"] = "-1"

        if attrs["tr_str_ped"] == "01":
            tags["toll"] = "yes"

        match attrs["tr_str_sed"]:
            case "02":
                tags["bridge"] = "yes"
                tags["layer"] = "1"
            case "0201":
                tags["bridge"] = "yes"
                tags["layer"] = "1"
            case "0202":
                tags["bridge"] = "yes"
                tags["layer"] = "2"
            case "03":
                tags["tunnel"] = "yes"
                tags["layer"] = "-1"

        match attrs["tr_str_sta"]:
            case "02":
                tags["construction"] = tags["highway"]
                tags["highway"] = "construction"
            case "03":
                tags["disused:highway"] = tags["highway"]
                del tags["highway"]

        match attrs["tr_str_ty"]:
            case "02":
                tags["highway"] = "footway" # Può anche essere steps
            case "04":
                tags["highway"] = tags["highway"] + "_link"

        return tags

