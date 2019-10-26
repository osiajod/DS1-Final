import urllib.request
import urllib.error
from urllib.parse import urlencode, quote_plus, quote
import json
import time
import re
import os
# import requests.exceptions
import random
# import requests
import geopandas
import geopy
from geopy.geocoders import Nominatim

from geocoding import google_keys
from geocoding import osm_keys




class GeoCrawler:

    def __init__(self):
        pass

    def sendRequest(self):
        pass

    def latlong_to_addr(self):
        pass

    def addr_to_latlong(self):
        pass

    def parseResult(self):
        pass
    def __str__(self):
        pass



class GoogleGeoCrawler(GeoCrawler):
    def __init__(self):
        super().__init__()
        self.keys = google_keys
        self.address_url = "https://maps.googleapis.com/maps/api/geocode/json?address="

    def addr_to_latlong(self, addr):
        rotated_id_index = random.randrange(0, len(self.keys))
        rand_key = self.keys[rotated_id_index]
        addr_and_key = self.address_url + addr + "Ca&key=" + rand_key
        try:
            response = requests.get(addr_and_key)
            response_json = response.json()
            return response_json
        except urllib.error.HTTPError as e:
            print("HTTPError has occured")
            time.sleep(1)
            self.addr_to_longlat(addr)

    def latlong_to_addr(self):
        pass


class OSMGeoCrawler(GeoCrawler):
    def __init__(self, set_to_region=""):
        """
        :param set_to_region: string address of city and the State where you want to localize your search. Shown to enhance accuracy.
        """
        super().__init__()
        self.region_search = "%s, "+set_to_region
        if len(self.region_search) != 3:
            self.locator = Nominatim(user_agent="DS1Geocoder", format_string=self.region_search)
        else:
            self.locator = Nominatim(user_agent="DS1Geocoder")

    def addr_to_latlong(self, str_address):
        """

        :param str_address:  The string expression of address. Most accurate when OSM Geocrawler is initialized with region_search set to "city_name, state_name"
        :return: Tuple of (lat, long) in floating points
        """
        location = self.locator.geocode(str_address)
        # print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        if location is not None:
            return (location.latitude, location.longitude)
        else:
            return None

    def latlong_to_addr(self, lat, long):
        """

        :param lat: floating point latitude
        :param long: floating point longitude
        :return:
            None if no result is found.
            Else, 1. nearest string address followed by
                  2. latitude floating point
                  3. longitude floating point
        """
        nearest_location =self.locator.reverse(str(lat)+", "+str(long))
        print(nearest_location.raw)
        if nearest_location is not None:
            return nearest_location.address, nearest_location.latitude, nearest_location.longitude
        else:
            return None

if __name__ == '__main__':
    # ggc = GoogleGeoCrawler()
    # print(ggc.addr_to_longlat("Harvard Square"))
    ogc = OSMGeoCrawler()
    lat_long = ogc.addr_to_latlong("24 Everett St, Cambridge")
    print(lat_long)
    print(ogc.latlong_to_addr(lat_long[0], lat_long[1]))
