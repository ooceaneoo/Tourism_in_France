import geopandas as gpd
sf = gpd.read_file('france-geojson/departements-version-simplifiee.geojson')
sf.head()