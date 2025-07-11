from flask import Blueprint

bp = Blueprint('recommended_bp', __name__)

import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
import logging, requests
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from dash import dcc

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/', suppress_callback_exceptions=True)

logging.basicConfig(filename="C:\\Users\\gauri\\IdeaProjects\\Real\\flaskr\\logs\\recommended_property.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# property_data = pd.read_csv('../recommendation/geocoded_address.csv')
property_data = pd.read_csv('C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\geocoded_address.csv')

dash_map = None

@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    property_data['price'] = property_data['price'].astype(str)
    property_data['total_area'] = property_data['total_area'].astype(str)
    property_data['price_per_sqft'] = property_data['price_per_sqft'].astype(str)
    property_data['baths'] = property_data['baths'].astype(str)
    property_data['balcony'] = property_data['balcony'].astype(str)

    # Create a new column 'similar_property' by concatenating other data
    property_data['similar_property'] = (property_data['name'] + ' ' + property_data['property_title'] + ' ' +
                                         property_data['price'] + ' ' + property_data['location'] + ' ' + property_data[
                                             'total_area'] + ' ' +
                                         property_data['price_per_sqft'] + ' ' + property_data['description'] + ' ' +
                                         property_data['baths'] +
                                         ' ' + property_data['balcony'])

    # Define the TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Fit and transform the 'content' column with the TF-IDF vectorizer
    tfidf_matrix = tfidf.fit_transform(property_data['similar_property'])

    # Compute the cosine similarity matrix
    cosine_similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    property_name = request.args.get('name')
    location = request.args.get('location')
    num_recs = int(request.args.get('num_recs', 50))  # default value is 50 if 'num_recs' is not provided
    property_index = property_data[property_data['name'] == property_name].index[0]
    similar_property = list(enumerate(cosine_similarity_matrix[property_index]))
    sorted_similar_property = sorted(similar_property, key=lambda x: x[1], reverse=True)[1:]
    # recomms = [property_data.iloc[i[0]]['name'] for i in sorted_similar_songs][:num_recs]
    recomms = []
    for i in range(num_recs):
        index = sorted_similar_property[i][0]
        property_info = {
            'property_id': int(property_data.iloc[index]['property_id']),
            'property_title': property_data.iloc[index]['property_title'],
            'price': str(property_data.iloc[index]['price']),
            'name_location': property_data.iloc[index]['name_location'],
            'latitude': property_data.iloc[index]['latitude'],
            'longitude': property_data.iloc[index]['longitude'],
            'price_value': property_data.iloc[index]['price_value']
        }
        recomms.append(property_info)
    print(recomms)
    for i in range(len(recomms)):
        logger.info(recomms)
    return jsonify(recomms)


# Function to fetch recommendations
def fetch_recommendations():
    response = requests.get(f'http://192.168.0.100:5000/get_recommendations?name=CasaGrand%20Vistaaz&recs=50')
    print("Response: ", response)
    if response.status_code == 200:
        print(response.status_code)
        return response.json()
    else:
        return []


# Callback for displaying the map
@dash_app.callback(
    dash.dependencies.Output('map-container', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
# recomms = fetch_recommendations()
def display_recommendations(pathname):
    print("Hi")
    global icon, dash_map
    # property_name = request.args.get('name')
    recomms = fetch_recommendations()
    print(recomms)
    red_icon = dict(
        iconUrl='https://cdn-icons-png.freepik.com/512/10263/10263405.png',
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        # iconUrl='https://w7.pngwing.com/pngs/904/527/png-transparent-several-assorted-color-gps-icons-point-euclidean-anchor-text-heart-technic-thumbnail.png',
        iconSize=[18, 45],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )
    blue_icon = dict(
        iconUrl='https://cdn-icons-png.freepik.com/512/5874/5874117.png',
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize=[18, 45],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )
    green_icon = dict(
        iconUrl='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9yr8EJi-Ofj58xl0EeWJ4H4geeqKz4t8wxw&s',
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize=[18, 45],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )
    orange_icon = dict(
        iconUrl='https://cdn.imgbin.com/12/3/24/imgbin-computer-icons-home-automation-kits-nonformal-education-others-VTZmRCdzC0q46YESZtjCPFbTc.jpg',
        # https://t4.ftcdn.net/jpg/05/47/85/83/360_F_547858382_5DSatutsFKB7onHW80N1Hnd1VoSuhdQg.jpg
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize=[38, 55],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )

    purple_icon = dict(
        iconUrl='https://cdn.iconscout.com/icon/premium/png-256-thumb/home-1822-1096104.png',
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize=[18, 45],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )

    yellow_icon = dict(
        iconUrl='https://www.pngfind.com/pngs/m/181-1818080_home-icon-home-icon-png-yellow-transparent-png.png',
        # shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize=[18, 45],
        shadowSize=[50, 64],
        iconAnchor=[22, 94],
        shadowAnchor=[4, 62],
        popupAnchor=[-3, -76]
    )
    markers = []
    for property_info in recomms:
        if int(property_info['price_value']) > 15000000:
            print("Red icon", property_info['price_value'])
            icon = red_icon
        if 10000000 < int(property_info['price_value']) < 15000000:
            print("Blue icon", property_info['price_value'])
            icon = blue_icon
        if 5000000 < int(property_info['price_value']) < 10000000:
            print("Purple icon", property_info['price_value'])
            icon = purple_icon
        if 2500000 < int(property_info['price_value']) < 5000000:
            print("Green icon", property_info['price_value'])
            icon = green_icon
        if int(property_info['price_value']) < 2500000:
            print("Yellow icon", property_info['price_value'])
            icon = yellow_icon

        markers.append(
            dl.Marker(
                id=str(property_info['property_id']),
                # icon=icons.greenIcon,
                position=[property_info['latitude'], property_info['longitude']],
                # price = int(property_info['price']),
                icon=icon,
                children=[
                    dl.Tooltip(property_info['name_location']),
                    dl.Popup(html.Div([
                        html.H3(property_info['property_title']),
                        html.P(f"Price: {property_info['price']}"),
                        html.P(property_info['name_location'])
                    ]))
                ],

                # if price>2.5:
                #     icon= red_icon
            )

            # for property_info in recomms

            # if int(property_info['price_value'])>10000000:
            #     icon = blue_icon
            # if int(property_info['price_value'])<10000000:
            #     icon = red_icon
        )

    center_latitude = sum(property_info['latitude'] for property_info in recomms) / len(recomms)
    center_longitude = sum(property_info['longitude'] for property_info in recomms) / len(recomms)

    colorscale = ['yellow', 'green', 'purple', 'blue', 'red']

    dash_map = dl.Map(
        id="map",
        center=[center_latitude, center_longitude],
        zoom=10,
        style={'width': '100%', 'height': '100vh', 'margin': '0', 'padding': '0'},
        children=[
            dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
            dl.Colorbar(colorscale=colorscale, width=20, height=200, min=0, max=15000000, position="bottomright"),
            # dl.SearchControl(position='topleft',placeholder='Search for a property...'),
            # dcc.Input(id='search-input', type='text', value=''),
            *markers
        ]
    )

    return dash_map


dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # Add the location component
    html.Div(id='map-container'),  # Container for the map
    html.Div([
        dash_map
    ])
])
# @dash_app.callback(
#     dash.dependencies.Output("layer", "children"),
#     [dash.dependencies.Input("search-button", "n_clicks")],
#     [dash.dependencies.State("search-input", "value")]
# )
# def update_map(n_clicks, value):
#     if n_clicks > 0 and value:
#         return [
#             dl.Marker(position=dl.GeoJSON(data=value))
#         ]
#     else:
#         return []

if __name__ == "__main__":
    # get_recommendations()
    # fetch_recommendations()
    # display_recommendations()
    app.run(host='192.168.6.77', port=5000, debug=True)

# http://192.168.0.105:5000/get_recommendations?name=DARSHAN%20HEIGHTS&recs=50
# http://192.168.0.104:5000/display_recommendations
