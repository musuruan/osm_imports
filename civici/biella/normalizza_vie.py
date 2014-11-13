#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
A translation function for the "Comune di Biella" address data named "biella_civici_od.zip"

The shapefiles are availble under the IODL 2.0 at:
http://www.comune.biella.it/sito/index.php?biella-open-data

Copyright (C) 2014 Andrea Musuruane <musuruan@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import csv
import normalizer

streetNames = {}

# Read toponyms
inputFile = open("elenco_viesit.csv", "rb")
streetReader = csv.DictReader(inputFile, delimiter=";")
fieldnames = streetReader.fieldnames

outputFile = open("elenco_viesit_osm.csv", "wb")
fieldnames.append("NOME_VIA_OSM")
streetWriter = csv.DictWriter(outputFile, fieldnames, delimiter=";")
streetWriter.writeheader()

for row in streetReader:
    row["NOME_VIA_OSM"] = normalizer.translateName(row["NOME_VIA"]).encode("utf-8")
    streetWriter.writerow(row)

inputFile.close()
outputFile.close()
