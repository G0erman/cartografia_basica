import csv
import fiona
from fiona.crs import from_epsg
import gdal
import os
from shapely.geometry import mapping, Point
import time


inputfile = os.path.realpath('./datos/APOYO_HONDURAS.csv')
output = os.path.realpath('./shapefiles/APOYOS.shp')

#proyeccion cartografica UTM 16 N
f_crs=from_epsg(32616)

# columnas contenidas en el archivo shapefile
schema = {
    'geometry': 'Point',
    'properties': {
                'CODIGOAPOYO'       :   'str:20',
                'PINTADOAPOYO'      :   'str:20',
                'X'                 :   'int:10',
                'Y'                 :   'int:10',
                'TIPONODO'          :   'str:2'
    }                
}

start = time.time()

with open(inputfile, newline='') as csvfile:
    with fiona.open(output,'w', driver='ESRI Shapefile', crs=f_crs, schema=schema) as c:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  #omitir la linea de cabecera
        for r in reader:
            point=Point(int(r[5]),int(r[4]))
            c.write({
                'geometry': mapping(point),
                'properties': {
                    'CODIGOAPOYO'   :   r[0],
                    'PINTADOAPOYO'  :   r[1],
                      'X'           :   int(r[5]),
                      'Y'           :   int(r[4]),
                      'TIPONODO': r[3]+r[2]
                       }
	})
print("proceso finalizado")

elapsed = (time.time() - start)
print(' TIEMPO TOTAL DE PROCESAMIENTO')
print ('		' + str(elapsed/60)+" Minutos")

