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
ogr2osm -t localita.py -f Vercelli_dbsn.gdb -o localita_VC.osm
"""

import ogr2osm
import string
from osgeo import ogr

def removeAbbreviations(name):
    name = name.replace("A. ", "Alpe ")
    name = name.replace("C. ", "Cascina ")
    name = name.replace("C.e ", "Case ")
    name = name.replace("C.lo ", "Castello ")
    name = name.replace("C.se ", "Case ")
    name = name.replace("C.na ", "Cascina ")
    name = name.replace("C.ne ", "Cascine ")
    name = name.replace("C.to ", "Casato ")
    name = name.replace("Casc.to ", "Cascinotto ")
    name = name.replace("M.o ", "Molino ")
    name = name.replace("S. Giov.i", "San Giovanni")
    name = name.replace("S. ", "San ")
    name = name.replace("Mad.na", "Madonna")
    name = name.replace("Inf.e", "Inferiore")
    name = name.replace("Inf.re", "Inferiore")
    name = name.replace("Inf.", "Inferiore")
    name = name.replace("Sup.e", "Superiore")
    name = name.replace("Sup.re", "Superiore")
    name = name.replace("Sup.", "Superiore")
    return name

class Translate(ogr2osm.TranslationBase):

    def filter_layer(self, layer):
        if layer.GetName() != ('loc_sg'):
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
        
        # Only "località" (01) but not "capoluogo" (0101) because these are already in OSM
        index = ogrfeature.GetFieldIndex('loc_sg_ty')
        if index >= 0:
            loc_sg_ty = ogrfeature.GetField(index)

        if not(loc_sg_ty.startswith('01') and not loc_sg_ty.startswith('0101')):
            return None

        # Return the centorid
        # Undocumented feature: https://github.com/roelderickx/ogr2osm/issues/53#issuecomment-3220486802
        ogrfeature.SetGeometry(ogrfeature.GetGeometryRef().Centroid())

        return ogrfeature

        
    def filter_tags(self, attrs):
        if not attrs:
            return

        tags = {}
        tags["name"] = attrs["loc_sg_top"]
        if tags["name"].isupper():
            tags["name"] = string.capwords(tags["name"])
        tags["name"] = removeAbbreviations(tags["name"])
        
        firstWord = tags["name"][: tags["name"].find(' ')]

        match attrs["loc_sg_ty"]:
            case "010201":
                tags["place"] = "hamlet"
            case "010202":
                tags["place"] = "hamlet"
            case "0103":
                if firstWord == "Cascina" or firstWord == "Cascine":
                    tags["place"] = "farm"
                else:
                    tags["place"] = "isolated_dwelling"
            case "0104":
                if firstWord == "Cascina" or firstWord == "Cascine":
                    tags["place"] = "farm"
                else:
                    tags["place"] = "isolated_dwelling"

        return tags

