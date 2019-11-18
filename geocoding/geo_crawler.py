import urllib.request
import urllib.error
from urllib.parse import urlencode, quote_plus, quote
import json
import time
import re
# import requests.exceptions
import random
# import requests
import geopandas
import geopy
from geopy.geocoders import Nominatim

from geocoding import google_keys
from geocoding import osm_keys
from pprint import pprint
import zipcodes
from geopy.exc import GeocoderTimedOut




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
            self.locator = Nominatim(user_agent="DS1Geocoder", format_string=self.region_search, timeout=3)
        else:
            self.locator = Nominatim(user_agent="DS1Geocoder", timeout=3)

    def addr_to_latlong(self, str_address):
        """

        :param str_address:  The string expression of address. Most accurate when OSM Geocrawler is initialized with region_search set to "city_name, state_name"
        :return: Tuple of (lat, long) in floating points
        """
        # zip_code = re.search(r'.*(\d{5}(\-\d{4})?)$', str_address)
        # zip_code = re.search(r"(.*\d{5}-\d{4}\b|.*\d{5})", str_address)

        regex = re.compile(r"[0-9]{5}(?:-[0-9]{4})?")

        matches = re.findall(regex, str_address)
        # print(matches)
        try:
            assert len(matches) == 1
            zip_code_str = matches[0]
            # zip_code_str = zip_code.groups()[0]
            print(f"*** zip_code_str:{zip_code_str}")
        except:
            zip_code_str = None

        if zip_code_str is not None:
            try:
                CITY = zipcodes.matching(zip_code_str)[0]["city"]
                City = CITY[:1] + CITY[1:].lower()
                str_address = str_address.replace(zip_code_str, City)
                print(str_address)

            except:
                print("No zipcode and/or cannot replace zipcode with city name.")


        try:
            location = self.locator.geocode(str_address)
        # print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        except GeocoderTimedOut:
            time.sleep(0.5)
            return self.addr_to_latlong(str_address)



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
        try:
            nearest_location =self.locator.reverse(str(lat)+", "+str(long))
        except GeocoderTimedOut:
            time.sleep(0.5)
            return self.latlong_to_addr(lat,long)

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

    ogc2 = OSMGeoCrawler("MA")
    lat_long2 = ogc2.addr_to_latlong("24 oxford st, 02138")
    print(lat_long2)
    print(ogc2.latlong_to_addr(lat_long2[0], lat_long2[1]))

    ogc3 = OSMGeoCrawler()
    lat_long3 = ogc3.addr_to_latlong("21 Burlington Ave, 02215")
    print(lat_long3)
    print(ogc3.latlong_to_addr(lat_long3[0], lat_long3[1]))

    ogc4 = OSMGeoCrawler()
    lat_long4 = ogc4.addr_to_latlong("78 Kirkland St, MA 02138-2033")
    print(lat_long4)
    print(ogc4.latlong_to_addr(lat_long4[0], lat_long4[1]))