'''
Convierte una lista de puntos en coordenadas cartesianas a geograficas
'''

import csv
import gdal
from shapely.geometry import mapping, Point
import fiona
from fiona.crs import from_epsg
import pyproj
from functools import partial
from shapely.ops import transform
import os


inputfile = os.path.realpath('./datos/APOYO_ESSA.csv')
output = os.path.realpath('./shapefiles/APOYOS_PROYECTADOS.shp')

#proyeccion cartografica wgs84 destino
f_crs=from_epsg(4326)

schema = {
    'geometry': 'Point',
    'properties': {
            'CODIGOAPOYO'       :   'str:8',  #>10
            'PINTADOAPOYO'      :   'str:8',
            'X'                 :   'int:10',
            'Y'                 :   'int:10',
            'CODIGOGEOGRAFICO'  :   'str:2'
    }                
}
# proyeccion cartografica
project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:3116'), # sistema coordenado origen
    pyproj.Proj(init='epsg:4326'))  # sistema coordenado destino



with open(inputfile, newline='') as csvfile:
    with fiona.open(output,'w', driver='ESRI Shapefile', crs=f_crs, schema=schema) as c:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  #omitir la linea de cabecera
        for r in reader:
            point=Point(int(r[2]),int(r[3]))
            point = transform(project, point)
            c.write({
                'geometry': mapping(point),
                'properties': {
                'CODIGOAPOYO'       :   r[0],
                'PINTADOAPOYO'      :   r[1],
                'X'                 :   int(r[2]),
                'Y'                 :   int(r[3]),
                'CODIGOGEOGRAFICO'  :   r[4]
            }
	})
print("proceso finalizado")


