Translation rules and other files needed to import into OpenStreetMap
the addresses provided by the Municipality of Torino (Italy).

Please read this wiki page for further information:
http://wiki.openstreetmap.org/wiki/Import/Catalogue/Address_import_for_Torino

Workflow:

$ wget http://aperto.comune.torino.it/sites/default/files/toponomastica_01062012.csv

$ csv2osm.py toponomastica_01062012.csv toponomastica_01062012.osm --csv-dialect excel-semicolon --lon longitudine --lat latitudine --csv-encoding latin1 --translator torino.py -f
