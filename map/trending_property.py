from flask import Blueprint, jsonify, Flask

bp = Blueprint('trending', __name__)

import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
import logging

app = Flask(__name__)
logging.basicConfig(filename="C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\logs\\trending_property.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# property_data = pd.read_csv('../recommendation/geocoded_address.csv')
property_data = pd.read_csv('C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\geocoded_address.csv')
def trending_property():
    random_data = property_data.sample(n=100)
    id = random_data['property_id']
    property_title = random_data['property_title']
    price = random_data['price']
    address = random_data['name_location']
    latitude = random_data['latitude']
    longitude = random_data['longitude']

    for i in range(len(random_data)):
        logger.info("ID: %s, ADDRESS: %s, LATITUDE: %s, LONGITUDE: %s",
                    id.iloc[i], address.iloc[i], latitude.iloc[i], longitude.iloc[i])
        # Assuming random_data is a DataFrame
    random_data_list = random_data.to_dict(orient='records')

    return random_data_list

# app = dash.Dash()
#
# markers = [
#     dl.Marker(
#         id=str(id.iloc[i]),
#         position=[latitude.iloc[i], longitude.iloc[i]],
#         children=[
#             dl.Tooltip(address.iloc[i]),
#             # dl.Popup(html.Div(address.iloc[i]))
#             dl.Popup(html.Div([
#                 html.H3(property_title.iloc[i]),
#                 html.P(f"Price: {price.iloc[i]}"),
#                 html.P(address.iloc[i])
#             ]))
#             # , property_title.iloc[i], price.iloc[i]
#             # , (property_title.iloc[i]), (price.iloc[i])
#         ]
#     )
#     for i in range(len(random_data))
# ]

# center_latitude = random_data['latitude'].mean()
# center_longitude = random_data['longitude'].mean()
#
# map = dl.Map(
#     id="map",
#     center=[center_latitude, center_longitude],
#     zoom=10,  # Adjust the zoom level as needed
#     style={'width': '100%', 'height': '100vh','margin': '0', 'padding': '0'},  # Set width and height to occupy the space
#     children=[
#         dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
#         *markers
#     ]
# )
#
# app.layout = html.Div([
#     map
# ])

# if __name__ == "__main__":
#     app.run_server(debug=True)
