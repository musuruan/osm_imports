#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import csv
import argparse
import os
import xml.etree.ElementTree as etree

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        raise argparse.ArgumentError("{0} does not exist".format(x))
    return x

# Parse command line
parser = argparse.ArgumentParser(description='Extract street names from an OSM XML file.')
parser.add_argument("-i", "--input",
    dest="filename", required=True, type=extant_file,
    help="input OSM XML file", metavar="FILE")
args = parser.parse_args()

streetnames = []
higways = {"primary", "secondary", "tertiary", "unclassified", "residential", "pedestrian"}

# Get all names in highways and addr:street
for event, elem in etree.iterparse(args.filename, events=["start"]):
    if elem.tag == "node" or elem.tag == "way":
        t = {}
        for item in elem.getchildren():
            if item.tag == "tag":
                k = item.attrib["k"]
                if k == "name":
                    t["name"] = item.attrib["v"]
                if k == "highway":
                    t["highway"] = item.attrib["v"]
                if k == "addr:street":
                    t["addr:street"] = item.attrib["v"]
                
        if "highway" in t and t["highway"] in higways and "name" in t and t["name"] not in streetnames:
            streetnames.append(t["name"])
        if "addr:street" in t and t["addr:street"] not in streetnames:
            streetnames.append(t["addr:street"])
    elem.clear() # won't need the children any more

streetnames.sort()

# Write street names
outputFile = open(os.path.splitext(args.filename)[0]+".csv", "wb")
fieldnames = ["NOME_VIA"]
streetWriter = csv.DictWriter(outputFile, fieldnames, delimiter=";")
streetWriter.writeheader()

for name in streetnames:
    row = {}
    row["NOME_VIA"] = name.encode("utf-8")
    streetWriter.writerow(row)

outputFile.close()
