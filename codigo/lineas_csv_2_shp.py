'''
Convertir lista de pares de puntos en archivo csv a linea
'''

import csv
import gdal
from shapely.geometry import mapping,LineString
import fiona
from fiona.crs import from_epsg
import pyproj
from functools import partial
from shapely.ops import transform
import os

inputfile = os.path.realpath('./datos/TRAMOBT_HONDURAS.csv')
output = os.path.realpath('./shapefiles/TRAMOSBT.shp')

f_crs=from_epsg(32616)

schema = {
	'geometry': 'LineString',
	'properties':{
		'TRAMO_MT'  :   'str:10',
		'ACOMETID'  :  	'str:10',
		'LONGITUD'  : 	'float:10.3'
	} 
}


with open(inputfile, newline='') as csvfile:
    with fiona.open(output,'w', driver='ESRI Shapefile', crs=f_crs, schema=schema) as c:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  #omitir la linea de cabecera
        for r in reader:
            line = LineString([(int(r[1]),int(r[2])) , (int(r[3]),int(r[4]))])
            LONGITUD = line.length
            c.write({
                'geometry': mapping(line),
                'properties':{
                    'TRAMO_MT'  :   r[0],
                    'ACOMETID'  :   r[6],
                    'LONGITUD'  :  LONGITUD
        }
	})
print("proceso finalizado")

