'''
copia un shapefile a otro, modificando el tamaño de un campo propiedad
'''

import fiona
import gdal
import os

inputfile = os.path.realpath('./shapefiles/APOYOS_PD.shp')
output = os.path.realpath('./shapefiles/APOYOS_PD_MOD.shp')

with fiona.open(inputfile, 'r') as source:
    # COPIA EL ESQUEMA DE LA FUENTE
    schema = source.schema.copy()
    schema['properties']['TIPONODO_C'] = 'str:3'

    # Create a sink for processed features with the same format and 
    # coordinate reference system as the source.
    with fiona.open(
            output, 'w',
            driver=source.driver,
            schema=schema,
            crs=source.crs
            ) as sink:
        
        for f in source:
            try:
                sink.write(f)
            except ValueError:  
                print("Error processing feature {}:".format(f['id']) )  