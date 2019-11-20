import pandas as pd
from uszipcode import SearchEngine


# result = search.by_coordinates(39.122229, -77.133578, radius=30, returns=5)
crime = pd.read_csv("./preposses_crimeda.csv")
search = SearchEngine(simple_zipcode=True)
# light = pd.read_csv("./")

def to_zipcode(lat_long_series):
    lat = lat_long_series[0]
    long = lat_long_series[1]
    return search.by_coordinates(lat,long,radius=30)[0].values()[0]

crime_zip = pd.DataFrame(crime[["Lat","Long"]].head().apply(to_zipcode, axis=1), columns=["zipcode"])

crime_zip.head()

crime_with_zip = pd.concat([crime, crime_zip], axis=1)
crime_with_zip.to_csv("crime_with_zip.csv", index=False)
print("finished converting crime")
#now do the same with Boston population
boston = pd.read_csv('./Boston_population_density.csv')
boston.rename(columns = {'Zipcode':'zipcode'}, inplace = True)

bldg = pd.read_csv('./bldg_zip.csv')
bldg.rename(columns = {'ZIPCODE' : 'zipcode'}, inplace = True)

land = pd.read_csv('./land_zip.csv')
land.rename(columns = {'ZIPCODE' : 'zipcode'}, inplace = True)

light = pd.read_csv('./streetlight_locations.csv')
light_zip = pd.DataFrame(light[["Lat","Long"]].apply(to_zipcode, axis=1), columns=["zipcode"])
light_with_zip = pd.concat([light, light_zip], axis=1)
light_with_zip.to_csv("light_with_zip.csv", index=False)
print("finished converting light")

crime_with_zip_joined = crime_with_zip.join(boston.set_index('zipcode'), on='zipcode')
crime_with_zip_joined = crime_with_zip_joined.join(bldg.set_index('zipcode'), on='zipcode')
crime_with_zip_joined = crime_with_zip_joined.join(land.set_index('zipcode'), on='zipcode')

crime_with_zip_joined.to_csv("crime_joined.csv", index=False)