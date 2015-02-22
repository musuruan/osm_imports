Translation rules and other files needed to import into OpenStreetMap
the addresses provided by the Municipality of Biella (Italy).

Please read this wiki page for further information:
https://wiki.openstreetmap.org/wiki/Import/Catalogue/Address_import_for_Biella

Workflow:

$ wget http://www.comune.biella.it/sito/file/biellaonline/open_data/biella_civici_od.zip

$ unzip data/biella_civici_od.zip

$ ./normalizza_vie.py

Manually edit "elenco_viesit_osm.csv" table to correct errors 

$ ogr2osm.py -t biella_civici_od.py biella_civici_od.shp

