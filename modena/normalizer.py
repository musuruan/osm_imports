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
__version__ = "2.0"
__date__ = "13 July 2015"

import re
import string

def translateName(streetName):
    lowercaseWords = [
        # Preposizioni
        "ai",
        "al",
        "alla",
        "alle",
        "d'",
        "da",
        "di",
        "de",
        "per",
        # Preposizioni articolate
        "dal",
        "della",
        "delle",
        "del",
        "dei",
        "dello",
        "degli",
        "dell'",
        # Congiunzioni
        "e",
        "ed",
        # Altre parole
        "antica",
        "privata",
        "vecchia"
        ]
    
    abbreviations = {
        "TRAV.": "TRAVERSA",
        "VIA IX GENNAIO 1950": "VIA 9 GENNAIO 1950",
        "VIA III FEBBRAIO" : "VIA 3 FEBBRAIO",
        "VIALE XXII APRILE" :"VIALE 22 APRILE",
        "PIAZZALE I MAGGIO": u"PIAZZALE 1° MAGGIO",
        "PIAZZA XX SETTEMBRE": "PIAZZA 20 SETTEMBRE",
        "VIALE IV NOVEMBRE": "VIALE 4 NOVEMBRE",
        "VIA TRENTASEIESIMO REGGIMENTO PISTOIA": u"VIA 36° REGGIMENTO PISTOIA"
    }
    
    # Remove abbreviations
    for abbreviation in abbreviations:
       streetName = streetName.replace(abbreviation, abbreviations[abbreviation])
    
    # Capitalize name
    streetName = streetName.strip().title()
    
    # Don't use capital letter for these words
    for word in lowercaseWords:
        if word[-1] != "'":
            word = word + " "
        match = word.title()
        streetName = streetName.replace(match, word)
  
    return streetName
    
