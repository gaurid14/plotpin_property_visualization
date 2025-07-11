# import googlemaps
import pandas as pd
from geopy import Photon
import logging
from flask import Blueprint
bp = Blueprint('geocoding', __name__)

# dataframe = pd.read_csv('sample_data.csv')
# geolocator = Photon(user_agent="geocoder")
logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class GeocodingAddress:
    def __init__(self):
        self.geolocator = Photon(user_agent="geocoder")
        self.dataframe = pd.read_csv('C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\real_estate_data.csv')
        # self.gmaps = googlemaps.Client(key = 'AIzaSyANL0uQCaHHxlmumQAeGLiwc0Hb0yVMO2Y')

    def geocode_all_address(self, location):
        try:
            result = self.geolocator.geocode(location)
            if result:
                latitude = result.latitude
                longitude = result.longitude
                # latitude = result[0]['geometry']['location']['lat']
                # longitude = result[0]['geometry']['location']['lng']
                logger.info("Latitude=%s, Longitude=%s", latitude,longitude)
                return latitude, longitude
            else:
                return None, None
        except Exception as e:
            logger.error(f"Error geocoding address {location}:{str(e)}")
            return None, None

    def geocode_csv(self):
        for index, row in self.dataframe.iterrows():
            print(f"Geocoding address {row['location']}...")
            latitude, longitude = self.geocode_all_address(row['location'])
            self.dataframe.at[index, 'latitude'] = latitude
            self.dataframe.at[index, 'longitude'] = longitude

        self.dataframe.to_csv('C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\geocoded_address.csv', index=False)
        print("CSV file created successfully")


# obj = GeocodingAddress()
# obj.geocode_csv()
