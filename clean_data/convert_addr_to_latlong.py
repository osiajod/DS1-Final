import pandas as pd
import csv

def convert_df_Addr(df, output_filename):
    output = []
    # count = 0
    for i in df_17_bldg['ADDR']:
        # if count % 500 == 0:
        #     print(count)
        # count = count + 1
        output.append(OSMGeoCrawler().addr_to_latlong(i))

    with open(output_filename, 'wb') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['LAT', 'LONG'])
        for row in output:
            csv_out.writerow(row)


df_17_bldg = pd.read_csv('2017_building_value.csv')
df_17_land = pd.read_csv('2017_land_value.csv')
df_18_bldg = pd.read_csv('2018_building_value.csv')
df_18_land = pd.read_csv('2018_land_value.csv')
df_19_bldg = pd.read_csv('2019_building_value.csv')
df_19_land = pd.read_csv('2019_land_value.csv')

convert_df_Addr(df_17_bldg, '2017_building_lat_long.csv')
convert_df_Addr(df_17_land, '2017_land_lat_long.csv')
convert_df_Addr(df_18_bldg, '2018_building_lat_long.csv')
convert_df_Addr(df_18_land, '2018_land_lat_long.csv')
convert_df_Addr(df_19_bldg, '2019_building_lat_long.csv')
convert_df_Addr(df_19_land, '2019_land_lat_long.csv')




df_17_LAT_LONG_land = []
# count = 0
for i in df_17_land['ADDR']:
    # if count % 500 == 0:
    #     print(count)
    # count = count + 1
    df_17_LAT_LONG_land.append(OSMGeoCrawler().addr_to_latlong(i))

with open('17_lat_long_land.csv','wb') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['LAT','LONG'])
    for row in df_17_LAT_LONG_land:
        csv_out.writerow(row)

df_16_LAT_LONG_bldg = []
# count = 0
for i in df_16_land['ADDR']:
    # if count % 500 == 0:
    #     print(count)
    # count = count + 1
    df_16_LAT_LONG_land.append(OSMGeoCrawler().addr_to_latlong(i))

with open('16_lat_long_bldg.csv','wb') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['LAT','LONG'])
    for row in df_16_LAT_LONG_land:
        csv_out.writerow(row)

df_16_LAT_LONG_land = []
# count = 0
for i in df_16_land['ADDR']:
    # if count % 500 == 0:
    #     print(count)
    # count = count + 1
    df_16_LAT_LONG_land.append(OSMGeoCrawler().addr_to_latlong(i))

with open('16_lat_long_bldg.csv','wb') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['LAT','LONG'])
    for row in df_16_LAT_LONG_land:
        csv_out.writerow(row)