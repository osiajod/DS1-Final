# import pandas as pd
# import time
#
# from geocoding.geo_crawler import OSMGeoCrawler
# df_17_bldg = pd.read_csv('../clean_data/2017_building_value.csv')
#
# count = 0
#
# df_17_LAT_LONG = []
#
# for i in df_17_bldg['ADDR']:
#     if count % 500 == 0:
#         print(count)
#     count = count +1
#     df_17_LAT_LONG.append(OSMGeoCrawler().addr_to_latlong(i))
#
# df_17_LAT_LONG = pd.DataFrame(df_17_LAT_LONG).to_csv('17_lat_long.csv')

import pandas as pd
import csv
from geocoding.geo_crawler import OSMGeoCrawler
import math
import os

def convert_df_Addr(df, output_filename, time_quota=False):
    output = []
    # count = 0
    for i in df['ADDR']:
        # if count % 500 == 0:
        #     print(count)
        # count = count + 1
        output.append(OSMGeoCrawler().addr_to_latlong(i, time_quota))

    pd.DataFrame(output).to_csv(output_filename, index=['LAT', 'LONG'])
    # with open(output_filename, 'wb') as out:
    #     csv_out = csv.writer(out)
    #     csv_out.writerow(['LAT', 'LONG'])
    #     for row in output:
    #         csv_out.writerow(row)


def partition_df(df, output_filename, num_per_part = 200, time_quota=False):
    df_list = []
    output_filename = output_filename.replace(".csv", "")
    for i in range(int(math.ceil((len(df)/200)))):
        if os.path.exists(output_filename + str(i) + ".csv"):
            continue
        df_list.append(df[i*num_per_part:min(i*num_per_part+num_per_part,len(df)-1)])

    for index, df in enumerate(df_list):
        convert_df_Addr(df, output_filename + str(index) + ".csv", time_quota)





# df_17_bldg = pd.read_csv('./clean_data/2017_building_value.csv')
# partition_df(df_17_bldg, './clean_data/2017_building_lat_long.csv')


# df_17_land = pd.read_csv('./clean_data/2017_land_value.csv')
# partition_df(df_17_bldg, './clean_data/2017_land_lat_long.csv')

df_18_bldg = pd.read_csv('./clean_data/2018_building_value.csv')
partition_df(df_18_bldg, './clean_data/2018_building_lat_long.csv', True)

# df_18_land = pd.read_csv('./clean_data/2018_land_value.csv')
# partition_df(df_18_land, './clean_data/2018_land_lat_long.csv')

df_19_bldg = pd.read_csv('./clean_data/2019_building_value.csv')
partition_df(df_19_bldg, './clean_data/2019_building_lat_long.csv', True)

# df_19_land = pd.read_csv('./clean_data/2019_land_value.csv')
# partition_df(df_19_land, './clean_data/2019_land_lat_long.csv')


# convert_df_Addr(df_17_bldg, './clean_data/2017_building_lat_long.csv')
# convert_df_Addr(df_17_land, './clean_data/2017_land_lat_long.csv')
# convert_df_Addr(df_18_bldg, './clean_data/2018_building_lat_long.csv')
# convert_df_Addr(df_18_land, './clean_data/2018_land_lat_long.csv')
# convert_df_Addr(df_19_bldg, './clean_data/2019_building_lat_long.csv')
# convert_df_Addr(df_19_land, './clean_data/2019_land_lat_long.csv')


