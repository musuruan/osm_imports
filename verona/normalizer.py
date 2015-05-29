# -*- coding: iso-8859-15 -*-

"""
Normalize street name using Italian OSM conventions:
https://wiki.openstreetmap.org/wiki/IT:Key:name

Copyright (C) 2014-2015 Andrea Musuruane <musuruan@gmail.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
Boston, MA  02110-1301, USA.
"""

__author__ = "Andrea Musuruane <musuruan@gmail.com>"
__version__ = "1.2"
__date__ = "29 May 2015"

import re
import sys

def translateName(streetName):
    words = [
        # Preposizioni
        "ai ",
        "al ",
        "alla ",
        "alle ",
        "d'",
        "da ",
        "di ",
        "de ",
        "per ",
        # Preposizioni articolate
        "dal ",
        "della ",
        "delle ",
        "del ",
        "dei ",
        "dello ",
        "degli ",
        "dell'",
        # Congiunzioni
        "e ",
        "ed ",
        # Altre parole
        "antica ",
        "privata ",
        "vecchia "
        ]
        
    abbreviations = {
        "COL.": "COLONNELLO",
        "F.LLI": "FRATELLI",
    }
    
    dug_abbreviations = {
        "C.DA": "CONTRADA",
        "C.LE": "CORTILE",
        "C.LLA": "CORTICELLA",
        "C.NE": "CIRCONVALLAZIONE",
        "C.SO": "CORSO",
        "G.RIA": "GALLERIA",
        "IN.TO": "INTERRATO",
        "L.GE": "LUNGADIGE",
        "L.GO": "LARGO",
        "P.LE": "PIAZZALE",
        "P.TTA": "PIAZZETTA",
        "P.TTI FONT.LLE": "PORTICHETTI FONTANELLE",
        "P.ZZA": "PIAZZA",
        "R.STE": "REGASTE",
        "S.DA": "STRADA",
        "S.LLA": "STRADELLA",
        "S.NE": "STRADONE",
        "S.TA": "SALITA",
        "SC.NE": "SCALONE",
        "SC.TA": "SCALETTA",
        "V.GIO": "VILLAGGIO",
        "V.LE": "VIALE",
        "V.LO": "VICOLO",
        "V.TTO": "VICOLETTO"
    }
    
    # Fix DUG (DUG = "denominazione urbanistica generica")
    for dug in dug_abbreviations:
        if streetName[:len(dug)+1] == dug + " ":
            streetName = dug_abbreviations[dug] + streetName[len(dug):]
            break
    
    # Remove abbreviations
    for abbreviation in abbreviations:
        streetName = streetName.replace(abbreviation, abbreviations[abbreviation])
    
    # Capitalize name
    streetName = streetName.strip().title()
    
    # Don't use capital letter for these words
    for word in words:
        streetName = streetName.replace(word.title(), word)
        
    # Full stop must be followed by a space
    streetName = re.sub(r"\.(\S)", r". \1", streetName)
  
    # Remove multiple spaces
    streetName = re.sub(r"\s\s+", " ", streetName)
    
    return streetName
    