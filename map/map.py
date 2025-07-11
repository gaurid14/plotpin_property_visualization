from flaskr.map import filtered_property, trending_property
import dash
from dash import html
import dash_leaflet as dl
from flask import Flask, jsonify, Blueprint, Response
from dash import dcc
import dash_bootstrap_components as dbc
import logging
import pandas as pd

bp = Blueprint('map', __name__)

# import filtered_property
# search_data = None
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# @bp.route('/explore')
def create_dash_app(flask_app):
    app = dash.Dash(__name__, server=flask_app, url_base_pathname='/map/explore/', external_stylesheets=[dbc.themes.BOOTSTRAP])

    logging.basicConfig(filename="C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\logs\\filters.log", format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    railway_stations_data = pd.read_csv(
        'C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\indian_railway_stations.csv')
    cities_data = pd.read_csv(
        'C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\indian_cities_database.csv')
    property_info = pd.read_csv(
        'C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\geocoded_address.csv')
    # city_railway_data =
    search_data = []
    amenities_data = []
    # min_price_data = []
    # max_price_data = []
    property_type_data = []
    baths_data = []
    # min_area_data = []
    # max_area_data = []
    furnish_data = []
    bedroom_data = []
    balcony_data = []
    transaction_data = []
    status_data = []
    possession_data = []

    colorscale = ['yellow', 'green', 'purple', 'blue', 'red']

    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
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


    # def apply_filters():
    #     recommendations = filtered_property.get_properties(search_data,amenities_data,min_price_data,max_price_data,property_type_data,baths_data,balcony_data,min_area_data,max_area_data,
    #                                                        furnish_data,bedroom_data,transaction_data,status_data,possession_data)
    #     return recommendations


    def create_markers(recomms):
        markers = []
        icon=None
        if isinstance(recomms, Response):
            # Extract the JSON data from the response
            recomms_data = recomms.json
        else:
            recomms_data = recomms  # Assume recomms is already in the correct format

        # Ensure recomms_data is iterable
        if isinstance(recomms_data, list):
            for property_info in recomms:
                if pd.isna(property_info['price_value']):
                    # Handle NaN values here. For example, you can continue to the next iteration
                    continue
                else:
                    price_value = str(property_info['price_value'])
                    if float(price_value) >= 15000000:
                        # print("Red icon", price_value)
                        icon = red_icon
                    elif 10000000 < float(price_value) < 15000000:
                        # print("Blue icon", price_value)
                        icon = blue_icon
                    elif 5000000 < float(price_value) < 10000000:
                        # print("Purple icon", price_value)
                        icon = purple_icon
                    elif 2500000 < float(price_value) < 5000000:
                        # print("Green icon", price_value)
                        icon = green_icon
                    elif float(price_value) <= 2500000:
                        # print("Yellow icon", price_value)
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
                                    html.P(property_info['name_location']),
                                    html.P(property_info['total_area']),
                                    html.P(property_info['possession']),
                                    html.P(property_info['status']),
                                    html.P(property_info['transaction'])
                                ]))
                            ],
                        )
                    )
            return markers

    # with app.server.app_context():
    #     # Call the trending_property function to get initial properties
    #     recomms = trending_property.trending_property()
    # markers = create_markers(recomms)


    # railway_stations=[]
    # for index, row in railway_stations_data.iterrows():
    #     railway_info = {
    #         'object_id': int(row['object_id']),
    #         'name': row['name'],
    #         'latitude': row['latitude'],
    #         'longitude': row['longitude'],
    #         'city':row['city']
    #     }
    #     railway_stations.append(railway_info)

    # for railway_station in railway_stations:
    #     markers.append(
    #         dl.CircleMarker(
    #             id=str(railway_station['object_id']),
    #             center=[railway_station['latitude'], railway_station['longitude']],
    #             radius=3,  # Adjust the radius as needed
    #             color="red",  # Adjust the color as needed
    #             children=[
    #                 dl.Tooltip(railway_station['name']),
    #                 dl.Popup(html.Div([
    #                     html.P(railway_station['name'])
    #                 ]))
    #             ],
    #         )
    #     )
    custom_map_layer = dl.TileLayer(url="https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=1fdff532b8304eaca0232b48ceeb686d", attribution='<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    normal_osm_layer = dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")

    layer_group = dl.LayerGroup([
        custom_map_layer,
        normal_osm_layer
    ])
    keys = ["osm", "transport", "crime_rate"]
    layer_control = dl.LayersControl(position="topright")
    map = dl.Map(
        id="map",
        zoom=5,
        # center=[19.022597926903504, 72.85464263939537],
        center=[23.0707,80.0982],
        maxBounds=[[6.7481, 68.1078], [35.5064, 97.3952]],
        style={'width': '100%', 'height': '100vh', 'marginTop': '30px', 'padding': '0'},
        children=[
            dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",attribution='<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
                              name='Osm',checked='osm')] +
                [dl.Overlay(dl.TileLayer(url="https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=1fdff532b8304eaca0232b48ceeb686d",attribution='<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
                            name='Transport')]
                # [dl.Overlay(dl.TileLayer(url="https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=1fdff532b8304eaca0232b48ceeb686d"),
                #               name='Crime Rate')],
                # [dl.Overlay(dl.LayerGroup(markers), name="markers", checked=True),
                #  dl.Overlay(dl.LayerGroup(polygon), name="polygon", checked=True)], id="lc"
            ),
            # layer_group,
            # dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",attribution='<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
            # dl.TileLayer(url="https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=1fdff532b8304eaca0232b48ceeb686d"),
            dl.Colorbar(colorscale=colorscale, width=20, height=200, min=0, max=15000000, position="bottomright"),
            dl.MeasureControl(position="bottomleft", primaryLengthUnit="kilometers",primaryAreaUnit="hectares",activeColor="#214097",completedColor="#972158"),
            dl.GestureHandling(),

            # *markers
        ],
    )

    app.layout = html.Div([
        html.Div([
            # dbc.Input(id='search-input', type='text', value='', placeholder='Search Property',
            #           style={'height': '35px', 'marginLeft': '10px', 'marginRight': '10px', 'width': '250px',
            #                  'padding': '15px', 'marginTop': '10px'}),
            # html.Button('Search', id='search-button', n_clicks=0, style={'height': '35px'})
            dcc.Dropdown(
                options=[{'label':i,'value':i} for i in cities_data['city']],
                id='search-dropdown',
                placeholder='Search location',
                searchable=True,
                clearable=True,
                multi=True,
            ),
            html.Div(id='search-output-container',style={'textAlign': 'center', 'marginTop': '30px', 'padding': '80px'})

        ], style={'position': 'absolute', 'top': '0px', 'left': '5px', 'width': '290px', 'height': '5px',
                  'padding': '6px'}),

        # html.Div([
        #     map
        # ], style={'position': 'relative', 'width': '100%', 'height': '100vh'}),

        html.Div([
            dcc.Dropdown(
                # ['Lift', 'Gymnasium', 'Visitor parking', 'Maintenance staff', 'Waste disposal', 'DTH television facility',
                #  'Jogging and strolling track', 'Road View'
                #  'Garden view', 'Kids play area', 'Fire fighting equipment', 'Lawn with pathway', 'Elder citizen club',
                #  'Security', 'Swimming pool', 'Club house', 'Guest house', 'Banquet hall', 'Gas pipeline'],
                options=[
                    {'label': 'Lift', 'value': 'lift'},
                    {'label': 'Gymnasium', 'value': 'gymnasium'},
                    {'label': 'Visitor Parking', 'value': 'visitor_parking'},
                    {'label': 'Maintenance Staff','value': 'maintenance_staff'},
                    {'label': 'Waste Disposal', 'value': 'waste_disposal'},
                    {'label': 'DTH Television Facility', 'value': 'dth_television_facility'},
                    {'label': 'Jogging Track', 'value': 'jogging_track'},
                    {'label': 'Road View', 'value': 'road_view'},
                    {'label': 'Garden View', 'value': 'garden_view'},
                    {'label': 'Kids Play Area', 'value': 'kids_play_area'},
                    {'label': 'Fire Fighting Equipment', 'value': 'fire_fighting_equipment'},
                    {'label': 'Elder Citizen Club', 'value': 'elder_citizen_club'},
                    {'label': 'Security', 'value': 'security'},
                    {'label': 'Swimming Pool', 'value': 'swimming_pool'},
                    {'label': 'Club House', 'value': 'club_house'},
                    {'label': 'Guest House', 'value': 'guest_house'},
                    {'label': 'Banquet Hall', 'value': 'banquet_hall'},
                    {'label': 'Gas Pipeline', 'value': 'gas_pipeline'}
                ],

                id='amenities-dropdown',
                placeholder='Select amenities...',
                searchable=False,
                clearable=True,
                multi=True
            ),
            html.Div(id='amenities-output-container', style={'textAlign': 'center', 'marginTop': '30px', 'padding': '80px'})

        ],
            style={'position': 'absolute', 'top': '0px', 'left': '290px', 'width': '460px', 'height': '5px',
                   'padding': '6px'}),

        html.Div([
            dcc.Dropdown(
                options=[
                    {'label': '0L', 'value': '0'},
                    {'label': '25L', 'value': '2500000'},
                    {'label': '50L', 'value': '5000000'},
                    {'label': '1Cr', 'value': '10000000'},
                    {'label': '1.5Cr', 'value': '15000000'},
                    {'label': '2Cr', 'value': '20000000'},
                    {'label': '2.5Cr', 'value': '25000000'},
                    {'label': '3Cr', 'value': '30000000'},
                    {'label': '4Cr', 'value': '40000000'},
                    {'label': '5Cr', 'value': '50000000'},
                    {'label': '6Cr', 'value': '60000000'},
                    {'label': '7Cr', 'value': '70000000'},
                    {'label': '8Cr', 'value': '80000000'},
                    {'label': '9Cr', 'value': '90000000'},
                    {'label': '10Cr', 'value': '100000000'}
                ],
                id='min-dropdown',
                placeholder='Min price',
                searchable=False,
                clearable=True,
                multi=False
            ),
            html.Div(id='min-output-container',
                     style={'textAlign': 'center', 'marginTop': '30px', 'padding': '80px', 'color': 'red'})

        ],
            style={'position': 'absolute', 'top': '0px', 'left': '750px', 'width': '110px', 'height': '5px',
                   'padding': '5px'}),

        html.Div([
            dcc.Dropdown(
                options=[
                    {'label': '0L', 'value': '0'},
                    {'label': '25L', 'value': '2500000'},
                    {'label': '50L', 'value': '5000000'},
                    {'label': '1Cr', 'value': '10000000'},
                    {'label': '1.5Cr', 'value': '15000000'},
                    {'label': '2Cr', 'value': '20000000'},
                    {'label': '2.5Cr', 'value': '25000000'},
                    {'label': '3Cr', 'value': '30000000'},
                    {'label': '4Cr', 'value': '40000000'},
                    {'label': '5Cr', 'value': '50000000'},
                    {'label': '6Cr', 'value': '60000000'},
                    {'label': '7Cr', 'value': '70000000'},
                    {'label': '8Cr', 'value': '80000000'},
                    {'label': '9Cr', 'value': '90000000'},
                    {'label': '10Cr', 'value': '100000000'},
                ],
                id='max-dropdown',
                placeholder='Max price',
                searchable=False,
                clearable=True,
                multi=False
            ),
            html.Div(id='max-output-container', style={'textAlign': 'center', 'marginTop': '30px', 'padding': '80px'})

        ],
            style={'position': 'absolute', 'top': '0px', 'left': '850px', 'width': '110px', 'height': '5px',
                   'padding': '5px'}),

        html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Flat', 'value': 'Flat'},
                    {'label': 'Villa', 'value': 'Villa'},
                    {'label': 'Independent House', 'value': 'Independent House'},
                ],
                id='property_type-dropdown',
                placeholder='Property Type',
                searchable=False,
                clearable=True,
                multi=True
            ),
            html.Div(id='property_type-output-container', style={'textAlign': 'center', 'marginTop': '30px', 'padding': '80px'}),
        ],
            style={'position': 'absolute', 'top': '0px', 'left': '960px', 'width': '200px', 'height': '5px',
                   'padding': '5px'}),
        html.Div([
            dbc.Button("Show more filters", id="show-more-filters", color="light", className="me-1", n_clicks=0),
        ],
            style={'position': 'absolute', 'top': '0px', 'left': '1200px', 'width': '200px', 'height': '5px',
                   'padding': '5px'}),

        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Baths"),
                            dcc.Dropdown(
                                options=[
                                    {'label': '1', 'value': '1'},
                                    {'label': '2', 'value': '2'},
                                    {'label': '3', 'value': '3'},
                                ],
                                id='baths-dropdown',
                                placeholder='Baths',
                                searchable=False,
                                clearable=True,
                                multi=False,
                                style={'width': '80px'}
                            ),
                            html.Div(id='baths-output-container',
                                     style={'left':'10px','textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ],
                        id="collapse-baths-filters",
                        is_open=False,
                        style={'marginRight': '5px'}
                    ),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Baths"),
                            dcc.Dropdown(
                                options=[
                                    {'label': '1BHK', 'value': '1 BHK'},
                                    {'label': '2BHK', 'value': '2 BHK'},
                                    {'label': '3BHK', 'value': '3 BHK'},
                                    {'label': 'Studio Independent House', 'value': 'Studio Independent House'},
                                    {'label': 'Any', 'value':''},
                                ],
                                id='bedroom-dropdown',
                                placeholder='Bedroom',
                                searchable=False,
                                clearable=True,
                                multi=False,
                                style={'width': '140px'}
                            ),
                            html.Div(id='bedroom-output-container',
                                     style={'textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ],
                        id="collapse-bedroom-filters",
                        is_open=False,
                        style={'marginRight': '10px'}
                    ),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Balcony"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'},
                                ],
                                id='balcony-dropdown',
                                placeholder='Balcony',
                                searchable=False,
                                clearable=True,
                                multi=False,
                                style={'width': '90px'}
                            ),
                            html.Div(id='balcony-output-container',
                                     style={'textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ],
                        id="collapse-balcony-filters",
                        is_open=False,
                        style={'marginRight': '5px'}
                    ),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            dcc.Dropdown(
                                options=[
                                    {'label': '0sqft', 'value': '0'},
                                    {'label': '500sqft', 'value': '500'},
                                    {'label': '1,000sqft', 'value': '1000'},
                                    {'label': '1,500sqft', 'value': '1500'},
                                    {'label': '2,000sqft', 'value': '2000'},
                                ],
                                id='min-area-dropdown',
                                placeholder='Min area',
                                searchable=False,
                                clearable=True,
                                multi=False,
                                style={'width': '100px'}
                            ),
                            html.Div(id='min-area-output-container',
                                     style={'textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-area-min-filters",
                        is_open=False,
                        style={'marginRight':'5px'}),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Property Area Max"),
                            # dbc.Input(id="property-area-max", type="number", min=0, step=1, placeholder="Max"),
                            dcc.Dropdown(
                                options=[
                                    {'label': '500sqft', 'value': '500'},
                                    {'label': '1,000sqft', 'value': '1000'},
                                    {'label': '1,500sqft', 'value': '1500'},
                                    {'label': '2,000sqft', 'value': '2000'},
                                    {'label': 'Any', 'value': ''},
                                ],
                                id='max-area-dropdown',
                                placeholder='Max area',
                                searchable=False,
                                clearable=True,
                                multi=False,
                                style={'width': '100px'}
                            ),
                            html.Div(id='max-area-output-container',
                                     style={'textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-area-max-filters", is_open=False),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Property Area Max"),
                            # dbc.Input(id="property-area-max", type="number", min=0, step=1, placeholder="Max"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'New', 'value': 'New'},
                                    {'label': 'Resale', 'value': 'Resale'},
                                ],
                                id='transaction-dropdown',
                                placeholder='Transaction',
                                searchable=False,
                                clearable=True,
                                multi=True,
                                style={'width': '120px'}
                            ),
                            html.Div(id='transaction-output-container',
                                     style={'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-transaction-filters", is_open=False),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Property Area Max"),
                            # dbc.Input(id="property-area-max", type="number", min=0, step=1, placeholder="Max"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Under Construction', 'value': 'Under Construction'},
                                    {'label': 'Ready to Move', 'value': 'Ready to Move'},
                                ],
                                id='status-dropdown',
                                placeholder='Status',
                                searchable=False,
                                clearable=True,
                                multi=True,
                                style={'width': '170px'}
                            ),
                            html.Div(id='status-output-container',
                                     style={'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-status-filters", is_open=False),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            # dbc.Label("Property Area Max"),
                            # dbc.Input(id="property-area-max", type="number", min=0, step=1, placeholder="Max"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Ready to Move', 'value': 'Ready to Move'},
                                    {'label': '2024', 'value': '2024'},
                                    {'label': '2025', 'value': '2025'},
                                    {'label': '2026', 'value': '2026'},
                                    {'label': '2027', 'value': '2027'},
                                ],
                                id='possession-dropdown',
                                placeholder='Possession',
                                searchable=False,
                                clearable=True,
                                multi=True,
                                style={'width': '140px'}
                            ),
                            html.Div(id='possession-output-container',
                                     style={'textAlign': 'center', 'marginTop': '40px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-possession-filters", is_open=False),
                ]),

                dbc.Col([
                    dbc.Collapse([
                        dbc.CardGroup([
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Unfurnished', 'value': 'Unfurnished'},
                                    {'label': 'Semi-furnished', 'value': 'Semi-furnished'},
                                    {'label': 'Fully furnished,', 'value': 'Fully furnished'},
                                ],
                                id='furnish-dropdown',
                                placeholder='Furnishing Type',
                                searchable=False,
                                clearable=True,
                                multi=True,
                                style={'width': '150px'}
                            ),
                            html.Div(id='furnish-output-container',
                                     style={'textAlign': 'center', 'marginTop': '30px', 'padding': '0px'})
                        ]),
                    ], id="collapse-property-furnish-filters",
                        is_open=False,
                        style={'marginRight':'5px'}),
                ]),
            ],
                style={'marginTop': '70px','display':'flex'}),
        ]),
        html.Div([map], style={'position': 'relative', 'width': '100%', 'height': 'calc(100vh - 56px)', 'marginTop': '26px'}),
        # html.Div(id='click-output-container')
    ])


    @app.callback(
        dash.dependencies.Output("collapse-baths-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-baths-filters", "is_open")],
    )
    def toggle_collapse_baths_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-bedroom-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-bedroom-filters", "is_open")],
    )
    def toggle_collapse_bedroom_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-balcony-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-balcony-filters", "is_open")],
    )
    def toggle_balcony_bedroom_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-area-min-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-area-min-filters", "is_open")],
    )
    def toggle_collapse_property_area_min_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-area-max-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-area-max-filters", "is_open")],
    )
    def toggle_collapse_property_area_max_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-transaction-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-transaction-filters", "is_open")],
    )
    def toggle_collapse_property_transaction_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-status-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-status-filters", "is_open")],
    )
    def toggle_collapse_property_status_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-possession-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-possession-filters", "is_open")],
    )
    def toggle_collapse_property_possession_filters(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        dash.dependencies.Output("collapse-property-furnish-filters", "is_open"),
        [dash.dependencies.Input("show-more-filters", "n_clicks")],
        [dash.dependencies.State("collapse-property-furnish-filters", "is_open")],
    )
    def toggle_collapse_property_area_max_filters(n, is_open):
        if n:
            return not is_open
        return is_open


    @app.callback(
        dash.dependencies.Output('search-output-container', 'children'),
        dash.dependencies.Input('search-dropdown', 'value')
    )
    def update_search_data(value):
        if value is None or len(value) == 0:  # Check if the dropdown is empty
            return html.Div('Please select at least one location.', style={'color': 'red'})
        else:
            print("Value: ",value)
            global search_data
            search_data=value if value else []
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            print("Array: ",search_data)
            logger.info(search_data)
            # return search_data
        return []

    @app.callback(
        dash.dependencies.Output('amenities-output-container', 'children'),
        dash.dependencies.Input('amenities-dropdown', 'value')
    )
    def update_amenities(value):
        if value is not None:
            print("Value: ",value)
            global amenities_data
            amenities_data=value
            update_map(search_data=search_data, amenities_data=amenities_data or [], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            print("Array: ",amenities_data)
            logger.info(f"Amenities: {amenities_data}")
            # return amenities_data
        return None


    @app.callback(
        dash.dependencies.Output('min-output-container', 'children'),
        dash.dependencies.Input('min-dropdown', 'value')
    )
    def update_min_price(value):
        if value is not None:
            global min_price_data
            min_price_data = value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=min_price_data, max_price_data=[])
            logger.info(f"Min price: {min_price_data}")
            # return min_price_data
        return None


    @app.callback(
        dash.dependencies.Output('max-output-container', 'children'),
        dash.dependencies.Input('max-dropdown', 'value')
    )
    def update_max_price(value):
        if value is not None:
            global max_price_data
            max_price_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=max_price_data)
            logger.info(f"Max price: {max_price_data}")
            # return max_price_data
        return None


    @app.callback(
        dash.dependencies.Output('property_type-output-container', 'children'),
        dash.dependencies.Input('property_type-dropdown', 'value')
    )
    def update_property_type(value):
        if value is not None:
            global property_type_data
            property_type_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=property_type_data, baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Property type: {property_type_data}")
            # return property_type_data
        return None


    @app.callback(
        dash.dependencies.Output('baths-output-container', 'children'),
        dash.dependencies.Input('baths-dropdown', 'value')
    )
    def update_baths_filter(value):
        if value is not None:
            global baths_data
            baths_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=baths_data, furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Baths: {baths_data}")
            # return baths_data
        return None

    @app.callback(
        dash.dependencies.Output('bedroom-output-container', 'children'),
        dash.dependencies.Input('bedroom-dropdown', 'value')
    )
    def update_bedroom_filter(value):
        if value is not None:
            global bedroom_data
            bedroom_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=bedroom_data, balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Bedroom: {bedroom_data}")
            # return bedroom_data
        return None

    @app.callback(
        dash.dependencies.Output('balcony-output-container', 'children'),
        dash.dependencies.Input('balcony-dropdown', 'value')
    )
    def update_balcony_filter(value):
        if value is not None:
            global balcony_data
            balcony_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=balcony_data, transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Balcony: {balcony_data}")
            # return balcony_data
        return None

    @app.callback(
        dash.dependencies.Output('min-area-output-container', 'children'),
        dash.dependencies.Input('min-area-dropdown', 'value')
    )
    def update_min_area(value):
        if value is not None:
            global min_area_data
            min_area_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=min_area_data, max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Min area: {min_area_data}")
            # return min_area_data
        return None


    @app.callback(
        dash.dependencies.Output('max-area-output-container', 'children'),
        dash.dependencies.Input('max-area-dropdown', 'value')
    )
    def update_max_area(value):
        if value is not None:
            global max_area_data
            max_area_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=max_area_data, min_price_data=[], max_price_data=[])
            logger.info(f"Max area: {max_area_data}")
            # return max_area_data
        return None

    @app.callback(
        dash.dependencies.Output('transaction-output-container', 'children'),
        dash.dependencies.Input('transaction-dropdown', 'value')
    )
    def update_transaction(value):
        if value is not None:
            global transaction_data
            transaction_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=transaction_data, status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Transaction: {transaction_data}")
            # return transaction_data
        return None

    @app.callback(
        dash.dependencies.Output('status-output-container', 'children'),
        dash.dependencies.Input('status-dropdown', 'value')
    )
    def update_status(value):
        if value is not None:
            global status_data
            status_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=status_data, possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Status: {status_data}")
            # return status_data
        return None

    @app.callback(
        dash.dependencies.Output('possession-output-container', 'children'),
        dash.dependencies.Input('possession-dropdown', 'value')
    )
    def update_possession(value):
        if value is not None:
            global possession_data
            possession_data=value
            update_map(search_data=search_data, amenities_data=None, property_type_data=[], baths_data=[], furnish_data=[], bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=possession_data, min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Possession: {possession_data}")
            # return possession_data
        return None

    @app.callback(
        dash.dependencies.Output('furnish-output-container', 'children'),
        dash.dependencies.Input('furnish-dropdown', 'value')
    )
    def update_furnish(value):
        if value is not None:
            global furnish_data
            furnish_data=value
            update_map(search_data=search_data, amenities_data=[], property_type_data=[], baths_data=[], furnish_data=furnish_data, bedroom_data=[], balcony_data=[], transaction_data=[], status_data=[], possession_data=[], min_area_data=[], max_area_data=[], min_price_data=[], max_price_data=[])
            logger.info(f"Furnish type: {furnish_data}")
            # return furnish_data
        return None

    @app.callback(
        dash.dependencies.Output('map', 'children'),
        [
            dash.dependencies.Input('search-dropdown', 'value'),
            dash.dependencies.Input('amenities-dropdown', 'value'),
            dash.dependencies.Input('min-dropdown', 'value'),
            dash.dependencies.Input('max-dropdown', 'value'),
            dash.dependencies.Input('property_type-dropdown', 'value'),
            dash.dependencies.Input('baths-dropdown', 'value'),
            dash.dependencies.Input('min-area-dropdown', 'value'),
            dash.dependencies.Input('max-area-dropdown', 'value'),
            dash.dependencies.Input('furnish-dropdown', 'value'),
            dash.dependencies.Input('bedroom-dropdown', 'value'),
            dash.dependencies.Input('balcony-dropdown', 'value'),
            dash.dependencies.Input('transaction-dropdown', 'value'),
            dash.dependencies.Input('status-dropdown', 'value'),
            dash.dependencies.Input('possession-dropdown', 'value'),
        ]
    )
    def update_map(search_data, amenities_data, min_price_data, max_price_data, property_type_data, baths_data,
                   min_area_data, max_area_data, furnish_data, bedroom_data, balcony_data, transaction_data, status_data, possession_data):
        search_data = search_data if search_data is not None else []
        amenities_data = amenities_data if amenities_data is not None else []
        property_type_data = property_type_data if property_type_data is not None else []
        baths_data = baths_data if baths_data is not None else []
        furnish_data = furnish_data if furnish_data is not None else []
        bedroom_data = bedroom_data if bedroom_data is not None else []
        balcony_data = balcony_data if balcony_data is not None else []
        transaction_data = transaction_data if transaction_data is not None else []
        status_data = status_data if status_data is not None else []
        possession_data = possession_data if possession_data is not None else []
        min_area_data = min_area_data if min_area_data is not None else []
        max_area_data = max_area_data if max_area_data is not None else []
        min_price_data = min_price_data if min_price_data is not None else []
        max_price_data = max_price_data if max_price_data is not None else []

        # Use the filter values to get the filtered properties
        print('search_data: ',search_data)
        print('amenities_data: ',amenities_data)
        print('property_type_data: ',property_type_data)
        print('baths_data: ',baths_data)
        print('furnish_data: ',furnish_data)
        print('bedroom_data: ',bedroom_data)
        print('balcony_data: ',balcony_data)
        print('transaction_data: ',transaction_data)
        print('status_data: ',status_data)
        print('possession_data: ',possession_data)
        print('min_area_data: ',min_area_data)
        print('max_area_data: ',max_area_data)
        print('min_price_data: ',min_price_data)
        print('max_price_data: ',max_price_data)
        # recomms = filtered_property.get_properties(
        #     search_data = search_data if search_data is not None else ['Chennai', 'Mumbai', 'Bangalore', 'Kolkata', 'New Delhi', 'Pune', 'Hyderabad'],
        #     amenities_data=amenities_data if amenities_data is not None else None,
        #     min_price_data=min_price_data if min_price_data is not None else None,
        #     # max_price_data=max_price_data if max_price_data[0] is not None else max_price_data,
        #     max_price_data = max_price_data if max_price_data is not None else float('inf'),
        #     property_type_data=property_type_data if property_type_data is not None else None,
        #     baths_data=baths_data if baths_data is not None else None,
        #     balcony_data=balcony_data if balcony_data is not None else None,
        #     min_area_data=min_area_data if min_area_data is not None else None,
        #     max_area_data=max_area_data if max_area_data is not None else 'inf',
        #     furnish_data=furnish_data if furnish_data is not None else None,
        #     bedroom_data=bedroom_data if bedroom_data is not None else None,
        #     transaction_data=transaction_data if transaction_data is not None else None,
        #     status_data=status_data if status_data is not None else None,
        #     possession_data=possession_data if possession_data is not None else None,
        # )
        recomms = filtered_property.get_properties(
            search_data=search_data,
            amenities_data=amenities_data,
            min_price_data=min_price_data,
            max_price_data=max_price_data,
            property_type_data=property_type_data,
            baths_data=baths_data,
            balcony_data=balcony_data,
            min_area_data=min_area_data,
            max_area_data=max_area_data,
            furnish_data=furnish_data,
            bedroom_data=bedroom_data,
            transaction_data=transaction_data,
            status_data=status_data,
            possession_data=possession_data
        )

        if not isinstance(recomms, list):
            print("Expected 'recomms' to be a list, but got a different type.")
            recomms = []  # Assign an empty list if recomms is not the expected type
        else:
            print("Mapping successful")
        # Create new markers based on the filtered properties
        new_markers = create_markers(recomms)
        # print("Mapping successful")
        # Return the updated children for the map, including the new markers
        return [
            *map.children[:-1],  # Keep all existing children except the old markers
            *new_markers  # Add the new markers
        ]
    return app


# if __name__ == "__main__":
#     import os
#     os.system("python recommended_property.py")
#     app.run(host='192.168.0.101', port=5000, debug=True)

# if __name__ == "__main__":
#     app.run_server(debug=True)
