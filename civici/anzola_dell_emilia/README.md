Translation rules and other files needed to import into OpenStreetMap
the addresses provided by the Municipality of Anzola dell'Emilia (Italy).

Please read this wiki page for further information:
http://wiki.openstreetmap.org/wiki/Import/Catalogue/Address_import_for_Anzola_dell_Emilia

Workflow:

$ wget http://dati.emilia-romagna.it/catalogodati/ricerca-avanzata/scarica.html?idallegato=101

$ unzip T4_Shp.zip

$ ogr2osm.py -t civici.py -e 3003 -f Civici.shp
