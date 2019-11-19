import folium
import pandas as pd
import pygeoj

boston_geo = pygeoj.load(filepath="ZIP_Codes.geojson")

# obtain zipcodes
boston_zipcodes = []
for feature in boston_geo:
    boston_zipcodes.append(feature.properties['ZIP5'])

# read csv
ma_data = pd.read_csv("MA_population_density.csv")

# convert to correct format and type
ma_data['Zipcode'] = '0' + ma_data['Zipcode'].astype(str)

# drop rows for zipcodes outside Boston
for zipcode in ma_data['Zipcode']:
    if zipcode not in boston_zipcodes:
        idx = ma_data.index[ma_data['Zipcode']==zipcode]
        ma_data.drop(idx, inplace=True)
        # print("dropped")

# define map
m = folium.Map(location=[42.3601, -71.0589], zoom_start=11)

# plot
folium.Choropleth(
    geo_data=boston_geo,
    name='choropleth',
    data=ma_data,
    columns=['Zipcode', 'Population density (per square mile of land area)'],
    key_on='feature.properties.ZIP5',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population density'
).add_to(m)

folium.LayerControl().add_to(m)

m.save("boston_population_density_map.html")

# path_prefix = '/Users/gengyichen/Desktop/ac209a/final project/'
#
# gdf = gpd.read_file(path_prefix + "zipcodes_nt/ZIPCODES_NT_POLY.shp")
#
# # convert to lat and long
# gdf = gdf.to_crs(epsg=4326)
# gdf = gdf.sort_values('POSTCODE')
#
# gdf["geometry"] = [MultiPolygon([feature]) for feature in gdf["geometry"]]
#
#
# gdf.to_file(path_prefix+"ma.json", driver='GeoJSON')
# ma_geo = pygeoj.load(filepath=path_prefix+"ma.json")
#
# ma_data = pd.read_csv(path_prefix+"MA_population_density.csv")
# ma_data['Zipcode'] = '0' + ma_data['Zipcode'].astype(str)
#
# m = folium.Map(location=[42, -71], zoom_start=8)
# folium.Choropleth(
#     geo_data=ma_geo,
#     name='choropleth',
#     data=ma_data,
#     columns=['Zipcode', 'Population density (per square mile of land area)'],
#     key_on='feature.properties.POSTCODE',
#     fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Population density'
# ).add_to(m)
#
# folium.LayerControl().add_to(m)
#
# m.save("map.html")
