# Library import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import seaborn as sns
import datetime
import folium #Geoploting library
from folium.plugins import HeatMap 
from folium import plugins
import geopandas as gpd
from matplotlib.pyplot import figure, show
from matplotlib.ticker import MaxNLocator
import os 
import pylab as pl
from IPython.display import HTML,display
import warnings
warnings.filterwarnings("ignore")
#%matplotlib inline




#List of columns to drop

def process_crimedata(df):
    columns_to_drop = ["INCIDENT_NUMBER", #Unneccecary
                    "OFFENSE_CODE", #Better to use group
                    "OFFENSE_DESCRIPTION", #Better to use group
                    "REPORTING_AREA", #Not needed
                    "UCR_PART", #Not needed
                    "Location"] #Loc and Lat columns are already there

    #Apply the column drop
    df.drop(columns_to_drop, axis=1, inplace=True)
    
    #drop some NA
    df=df.loc[(df['Lat']>35)&(df['Long']< -60)] #remove NA from 'Lat' and 'Long'
    df=df.dropna(subset=["STREET"])

    #Replace the -1 in the Lat & Long column with NaN
    df["Lat"].replace(-1,np.nan,inplace=True)
    df["Lat"].replace(-1,np.nan,inplace=True)

    #Adding a "No" to the shooting column
    df["SHOOTING"].fillna("N", inplace=True)

    #Converting to datetime
    df["OCCURRED_ON_DATE"] = pd.to_datetime(df["OCCURRED_ON_DATE"])

    

    #Renaming some crimes
    rename_crimes = {"INVESTIGATE PERSON": "Investigate Person",
                            "HUMAN TRAFFICKING" : "Human Trafficking",
                            "HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE": "Involuntary Servitude"}
    df["OFFENSE_CODE_GROUP"].replace(rename_crimes,inplace=True)

    return df


def feature_overview(df, feature_name, save = False):
    if feature_name == 'year':
        g= sns.catplot(x="YEAR", kind="count", palette="Blues",height = 5, aspect=7/5, data=df)
        axes = g.axes.flatten()
        axes[0].set_title('crime count each year')
        if save:
            g.savefig('EDA/year.jpg')
    if feature_name == 'month':
        
        g = sns.catplot(x="MONTH", hue="YEAR", kind="count", \
        palette="Paired",height = 5, aspect=7/5, data=df)
        axes = g.axes.flatten()
        axes[0].set_title('crime count by month')
        if save:
            g.savefig('EDA/month.jpg')

    if feature_name == 'day_of_week':
        day_order = ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday" ]
        plt.figure(figsize = (10,6))
        g = sns.countplot("DAY_OF_WEEK", data=df,order=day_order)
        plt.title('crime count by the day of week')
        if save:
            plt.savefig('EDA/weekday.jpg')

    if feature_name =='hour':
        plt.figure(figsize = (10,6))
        g = sns.countplot("HOUR",data=df)
        plt.title('crime count by hour')
        if save:
            plt.savefig('EDA/weekday.jpg')

    if feature_name =='crime_type':
        type={label: idx for idx, label in enumerate(np.unique(df['OFFENSE_CODE_GROUP']))}
        df['type']=df['OFFENSE_CODE_GROUP'].map(type) #change crime type to number
        print(type)
        index=pd.Index(df['type'])
        plt.figure(figsize = (10,6))
        plt.bar(index.value_counts().index,index.value_counts())
        plt.xlabel("Crime type")
        plt.ylabel("Count")
        plt.title("Counting for Crime type")

        if save:
            plt.savefig('EDA/crime_type.jpg')


    if feature_name =='crime_type_top10':
        plt.figure(figsize = (10,6))
        sns.countplot(y = df["OFFENSE_CODE_GROUP"],order=df["OFFENSE_CODE_GROUP"].value_counts()[:10].index)
        plt.suptitle("Most frequent crimes on Christmas", fontsize=15, fontweight=0, color='black', style='italic')
        plt.ylabel("Crime Type", fontsize=14)
        plt.xlabel("Total Crimes", fontsize=14)
        plt.tick_params(labelsize=12)

        if save:
            plt.savefig('EDA/crime_type_top10.jpg')

    
def geomap(df, year):

    """
    show first 2000 data in df
    year - int number representing year
    """
    
    #incidents=folium.map.FeatureGroup()
    Lat=42.3
    Lon=-71.1

    data1=df[df['YEAR']==year][0:2000]
    boston_map=folium.Map([Lat,Lon],zoom_start=12)
    incidents2=plugins.MarkerCluster().add_to(boston_map)
    for lat,lon,label in zip(data1.Lat,data1.Long,data1.OFFENSE_CODE_GROUP):
        folium.Marker(location=[lat,lon],icon=None,popup=label).add_to(incidents2)
    boston_map.add_child(incidents2)
    display(boston_map)
    plt.show()

def heatmap(df, year):
    christmas_crime = df[df['YEAR'] == year]
    christmas_crime_map = folium.Map(location=[42.3601, -71.0589],
                zoom_start = 12)
    christmas_crime_loc = christmas_crime[["Lat", "Long"]]
    christmas_crime_loc.dropna(inplace=True)
    HeatMap(christmas_crime_loc, radius = 20).add_to(christmas_crime_map)
    display(christmas_crime_map)

def main():
    #Importing the dataset
    df = pd.read_csv(r"./data/crimedata.csv",encoding = 'unicode_escape')
    df= process_crimedata(df)
    #feature_overview(df, 'hour')
    #heatmap(df, 2019)
    geomap(df, 2019)

#main()





    


