Translation rules and other files needed to import into OpenStreetMap
the addresses provided by Regione Emilia-Romagna (Italy).

Please read this wiki page for further information:
http://wiki.openstreetmap.org/wiki/IT:Emilia_Romagna_import_numeri_civici_2016


ogr2ogr is provided by gdal. In Fedora, install it with:
# dnf install gdal


Workflow (based on Piacenza data):

# Download source shp file
$ wget http://geoportale.regione.emilia-romagna.it/it/download/dati-e-prodotti-cartografici-preconfezionati/database-topografico/tutti-download-preconfezionati/dati_dbtr_V_NCV_GPT_Piacenza.zip

# Unzip data
$ unzip dati_dbtr_V_NCV_GPT_Piacenza.zip

# Convert shp file to UTF-8
$ export SHAPE_ENCODING="ISO-8859-1"
$ ogr2ogr piacenza.shp V_NCV_GPT.shp -lco ENCODING=UTF-8

# Traslate address data to OSM file format
$ ogr2osm.py -t civici.py -e 25832 -f piacenza.shp
