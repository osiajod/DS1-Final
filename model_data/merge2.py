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

def to_zipcode(lat, long):
    return search.by_coordinates(lat,long,radius=30)[0].values()[0]

# crime_zip = pd.DataFrame(crime[["Lat","Long"]].apply(to_zipcode, axis=1), columns=["zipcode"])
crime_zip = pd.DataFrame(crime[["Lat", "Long"]]).values
crime_zip_new = []

for lat, long in crime_zip:
    # print(to_zipcode(lat,long))
    crime_zip_new.append(to_zipcode(lat,long))


crime_zip = pd.DataFrame(crime_zip_new, columns=["zipcode"])
# print(crime_zip)

crime_with_zip = pd.concat([crime, crime_zip], axis=1)
crime_with_zip.to_csv("crime_with_zip.csv", index=False)

print("exporting crime finished")

#now do the same with Boston population
boston = pd.read_csv('./Boston_population_density.csv')
boston['Zipcode']='0'+boston['Zipcode'].astype(str)
boston.rename(columns = {'Zipcode':'zipcode'}, inplace = True)

bldg = pd.read_csv('./bldg_zip.csv')
bldg['ZIPCODE']='0'+bldg['ZIPCODE'].astype(str)
bldg.rename(columns = {'ZIPCODE' : 'zipcode'}, inplace = True)

land = pd.read_csv('./land_zip.csv')
land['ZIPCODE']='0'+land['ZIPCODE'].astype(str)
land.rename(columns = {'ZIPCODE' : 'zipcode'}, inplace = True)

light = pd.read_csv('./streetlight_locations.csv')

light_zip = pd.DataFrame(light[["Lat", "Long"]]).values
light_zip_new = []
for lat, long in light_zip:
    light_zip_new.append(to_zipcode(lat,long))

light_zip = pd.DataFrame(light_zip_new, columns=["zipcode"])

# light_zip = pd.DataFrame(light[["Lat","Long"]].apply(to_zipcode, axis=1), columns=["zipcode"])
light_with_zip = pd.concat([light, light_zip], axis=1)
light_with_zip.to_csv("light_with_zip.csv", index=False)

print("exporting light finished")


crime_with_zip_joined = crime_with_zip.join(boston.set_index('zipcode'), on='zipcode')
crime_with_zip_joined = crime_with_zip_joined.join(bldg.set_index('zipcode'), on='zipcode')
crime_with_zip_joined = crime_with_zip_joined.join(land.set_index('zipcode'), on='zipcode')

crime_with_light = crime_with_zip_joined.join(light_with_zip.set_index('zipcode'), on='zipcode')

crime_with_zip_joined.to_csv("crime_joined.csv", index=False)
crime_with_light.to_csv("crime_all_joined.csv", index=False)


