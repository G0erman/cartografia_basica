from fiona.crs import from_epsg
import geopandas
import os
import pandas as pd
from shapely.geometry import Point
import time


inputfile = os.path.realpath('./datos/APOYO_HONDURAS.csv')
output = os.path.realpath('./shapefiles/APOYOS_PD.shp')

data = pd.read_csv(inputfile,delimiter=';')

#proyeccion cartografica UTM 16 N
f_crs=from_epsg(32616)

start = time.time()

# combine lat and lon column to a shapely Point() object
data['geometry'] = data.apply(lambda x: Point((float(x.XR), float(x.YR))), axis=1)


point = geopandas.GeoDataFrame(data, geometry='geometry') # puntos
point.crs = f_crs
point.to_file(driver = 'ESRI Shapefile', filename= output)
print("proceso finalizado")

elapsed = (time.time() - start)
print(' TIEMPO TOTAL DE PROCESAMIENTO')
print ('		' + str(elapsed/60)+" Minutos")

# Let's take a copy of our layer
#data_proj = point.copy()

# Reproject the geometries by replacing the values with projected ones
#data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=4326)
#data_proj.crs = from_epsg(4326)
#data_proj.to_file(driver = 'ESRI Shapefile', filename= "result_proj.shp")


#print(data_proj.crs)