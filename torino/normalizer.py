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
__version__ = "1.1"
__date__ = "26 January 2015"

import roman
import re

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
        "Pza ": "Piazza "
    }
    
    months = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    
    # Capitalize name
    streetName = streetName.strip().title()

    # Remove abbreviations
    for abbreviation in abbreviations:
        streetName = streetName.replace(abbreviation, abbreviations[abbreviation])
    
    # Don't use capital letter for these words
    for word in words:
        streetName = streetName.replace(word.title(), word)
        
    # Full stop must be followed by a space
    streetName = re.sub(r"\.(\S)", r". \1", streetName)

    # Handle dates:
    #   the first day of the month is "1°" and not "Primo"
    #   days must not be written using roman numerals
    #   months must be lowercase

    words = streetName.split()
    
    for idx, word in enumerate(words):
        if word.lower() in months:
            prev_word = words[idx-1].upper()
            # Roman numerals
            if re.match("^X{0,3}(IX|IV|V?I{0,3})$", prev_word) is not None:
                words[idx-1] = str(roman.fromRoman(prev_word));
                words[idx] = word.lower()
            if prev_word == "PRIMO":
                words[idx-1] = u"1°"
                words[idx] = word.lower()
    
    streetName = ' '.join(words)
    
    return streetName
    
