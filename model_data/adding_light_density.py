import pandas as pd

crime_all_joined = pd.read_csv("crime_all_joined.csv")
crime_all_joined["zipcode"] ='0'+crime_all_joined['zipcode'].astype(str)


light_density_with_zip = pd.read_csv("light_density_with_zip.csv")
light_density_with_zip["zipcode"] ='0'+light_density_with_zip['zipcode'].astype(str)


crime_all_with_zip_light_density = crime_all_joined.join(light_density_with_zip.set_index('zipcode'), on='zipcode')



crime_all_with_zip_light_density = crime_all_with_zip_light_density.loc[:, crime_all_with_zip_light_density.columns != 'light_count']
crime_all_with_zip_light_density.loc[:, crime_all_with_zip_light_density.columns != 'Unnamed: 0'].to_csv('crime_light_density.csv')






