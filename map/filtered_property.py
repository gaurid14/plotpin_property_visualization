import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import jsonify, request, Blueprint
import logging

bp = Blueprint('filtered_property_bp', __name__)

logging.basicConfig(filename="C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\logs\\filtered_property.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Load the property data
property_data = pd.read_csv('C:\\Users\\gauri\\IdeaProjects\\Real Estate\\flaskr\\csv_data\\geocoded_address.csv')

# Ensure 'price_value' and 'total_area' are in a numerical data type for filtering
property_data['price_value'] = property_data['price_value'].replace('[\$,]', '', regex=True).astype(float)
property_data['total_area'] = property_data['total_area'].replace('[sqft]', '', regex=True).astype(float)

def get_properties(search_data, amenities_data, min_price_data, max_price_data, property_type_data, baths_data, balcony_data,
                   min_area_data, max_area_data, furnish_data, bedroom_data, transaction_data, status_data, possession_data):
    if search_data is not None:
        # Filter based on city
        filtered_data = property_data[property_data['city'].isin(search_data)]
        # Use the filter values to get the filtered properties
        print('***************Start******************************')
        print('search_data1: ',search_data)
        print('amenities_data1: ',amenities_data)
        print('property_type_data1: ',property_type_data)
        print('baths_data1: ',baths_data)
        print('furnish_data1: ',furnish_data)
        print('bedroom_data1: ',bedroom_data)
        print('balcony_data1: ',balcony_data)
        print('transaction_data1: ',transaction_data)
        print('status_data1: ',status_data)
        print('possession_data1: ',possession_data)
        print('min_area_data1: ',min_area_data)
        print('max_area_data1: ',max_area_data)
        print('min_price_data1: ',min_price_data)
        print('max_price_data1: ',max_price_data)
        print('*******************End**************************')

        # Apply filters one by one
        if property_type_data:
            filtered_data = filtered_data[filtered_data['property_type'].isin(property_type_data)]
            print("Property type: ",filtered_data.head())  # Print the filtered data

        if baths_data:
            filtered_data = filtered_data[(filtered_data['baths'].astype(int) >= int(baths_data[0]))]
            #print("Data1:",filtered_data[filtered_data['baths']])
            print("Baths: ",filtered_data.head())  # Print the filtered data

        if balcony_data:
            filtered_data = filtered_data[filtered_data['balcony']==balcony_data]
            print("Balcony: ",filtered_data.head())  # Print the filtered data

        if min_price_data:
            filtered_data = filtered_data[(filtered_data['price_value'].astype(int) >= int(min_price_data))]
            print("Min price: ",filtered_data.head())  # Print the filtered data

        if max_price_data:
            filtered_data = filtered_data[(filtered_data['price_value'].astype(int) <= int(max_price_data))]
            print("Max price: ",filtered_data.head())  # Print the filtered data

        if max_price_data and min_area_data:
            filtered_data = filtered_data[(filtered_data['price_value'].astype(int) >= int(min_price_data))]
            filtered_data = filtered_data[(filtered_data['price_value'].astype(int) <= int(max_price_data))]
            print("Min-Max price: ",filtered_data.head())

        if min_area_data:
            filtered_data = filtered_data[(filtered_data['total_area'].astype(int) >= int(min_area_data))]
            print("Min area: ",filtered_data.head())  # Print the filtered data

        if max_area_data:
            filtered_data = filtered_data[(filtered_data['total_area'].astype(int) <= int(max_area_data))]
            print("Max area: ",filtered_data.head())  # Print the filtered data

        if min_area_data and max_area_data:
            filtered_data = filtered_data[(filtered_data['total_area'].astype(int) >= int(min_area_data))]
            filtered_data = filtered_data[(filtered_data['total_area'].astype(int) <= int(max_area_data))]
            print("Min-Max Area: ",filtered_data['total_area'])

        if furnish_data:
            filtered_data = filtered_data[filtered_data['furnish_type'].isin(furnish_data)]
            print("Furnish: ",filtered_data.head())  # Print the filtered data

        if bedroom_data:
            filtered_data = filtered_data[filtered_data['bedroom']==(bedroom_data)]
            print("Bedroom: ",filtered_data.head())  # Print the filtered data

        if transaction_data:
            filtered_data = filtered_data[filtered_data['transaction'].isin(transaction_data)]
            print("Transaction: ",filtered_data.head())  # Print the filtered data

        if status_data:
            filtered_data = filtered_data[filtered_data['status'].isin(status_data)]
            print("Status: ",filtered_data.head())  # Print the filtered data

        if possession_data:
            filtered_data = filtered_data[filtered_data['possession'].isin(possession_data)]
            print("Possession: ",filtered_data.head())  # Print the filtered data

        if amenities_data:
            filtered_data = filtered_data[filtered_data['amenities'].apply(lambda x: any(amenity.strip() in x.split(',') for amenity in amenities_data))]
            print("Amenities: ",filtered_data.head())  # Print the filtered data

        print("Filtered data: ",filtered_data['price_value'])

        # Convert numerical columns to string data type
        if 'price_value' in filtered_data.columns:
            filtered_data['price_value'] = filtered_data['price_value'].astype(str)
        if 'total_area' in filtered_data.columns:
            filtered_data['total_area'] = filtered_data['total_area'].astype(str)
        if 'price_per_sqft' in filtered_data.columns:
            filtered_data['price_per_sqft'] = filtered_data['price_per_sqft'].astype(str)
        if 'baths' in filtered_data.columns:
            filtered_data['baths'] = filtered_data['baths'].astype(str)
        if 'balcony' in filtered_data.columns:
            filtered_data['balcony'] = filtered_data['balcony'].astype(str)

        # Combine all filtered data
        if not filtered_data.empty:
            # Convert filtered data to a list of dictionaries
            filtered_property = filtered_data.to_dict('records')

            filtered_property_df = pd.DataFrame(filtered_property)
            if 'price_value' in filtered_property_df.columns:
                filtered_property_df['price_value'] = filtered_property_df['price_value'].astype(str)
            if 'total_area' in filtered_property_df.columns:
                filtered_property_df['total_area'] = filtered_property_df['total_area'].astype(str)
            if 'price_per_sqft' in filtered_property_df.columns:
                filtered_property_df['price_per_sqft'] = filtered_property_df['price_per_sqft'].astype(str)
            if 'baths' in filtered_property_df.columns:
                filtered_property_df['baths'] = filtered_property_df['baths'].astype(str)
            if 'balcony' in filtered_property_df.columns:
                filtered_property_df['balcony'] = filtered_property_df['balcony'].astype(str)

            # Create a new column 'similar_property' by concatenating other data
            similar_property = ''
            if 'name' in filtered_property_df.columns:
                similar_property += filtered_property_df['name'] + ' '
            if 'property_title' in filtered_property_df.columns:
                similar_property += filtered_property_df['property_title'] + ' '
            if 'price_value' in filtered_property_df.columns:
                similar_property += filtered_property_df['price_value'].astype(str) + ' '
            if 'location' in filtered_property_df.columns:
                similar_property += filtered_property_df['location'] + ' '
            if 'total_area' in filtered_property_df.columns:
                similar_property += filtered_property_df['total_area'].astype(str) + ' '
            if 'price_per_sqft' in filtered_property_df.columns:
                similar_property += filtered_property_df['price_per_sqft'].astype(str) + ' '
            if 'description' in filtered_property_df.columns:
                similar_property += filtered_property_df['description'] + ' '
            if 'baths' in filtered_property_df.columns:
                similar_property += filtered_property_df['baths'].astype(str) + ' '
            if 'amenities' in filtered_property_df.columns:
                similar_property += filtered_property_df['amenities'] + ' '
            if 'balcony' in filtered_property_df.columns:
                similar_property += filtered_property_df['balcony'].astype(str) + ' '
            if 'status' in filtered_property_df.columns:
                similar_property += filtered_property_df['status'] + ' '
            if 'bedroom' in filtered_property_df.columns:
                similar_property += filtered_property_df['bedroom'].astype(str) + ' '
            if 'possession' in filtered_property_df.columns:
                similar_property += filtered_property_df['possession'] + ' '
            if 'furnish_type' in filtered_property_df.columns:
                similar_property += filtered_property_df['furnish_type'] + ' '
            if 'transaction' in filtered_property_df.columns:
                similar_property += filtered_property_df['transaction'] + ' '

            filtered_property_df['similar_property'] = similar_property
            print("Filtered data1: ",filtered_property_df)
            print("Filtered data: ",filtered_property_df['similar_property'])

            if not filtered_property_df['similar_property'].empty and any(filtered_property_df['similar_property']):
                # Define the TF-IDF vectorizer
                tfidf = TfidfVectorizer(stop_words='english')

                # Fit and transform the 'similar_property' column with the TF-IDF vectorizer
                tfidf_matrix = tfidf.fit_transform(filtered_property_df['similar_property'])

                # Compute the cosine similarity matrix
                cosine_similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
                property_index = filtered_property_df.index[0]
                num_recs = int(request.args.get('num_recs', 50))  # default value is 50 if 'num_recs' is not provided
                similar_property = list(enumerate(cosine_similarity_matrix[property_index]))
                sorted_similar_property = sorted(similar_property, key=lambda x: x[1], reverse=True)[1:]
                recomms = []
                if sorted_similar_property:
                    for i in range(len(sorted_similar_property)):
                        #print(i)
                        index = sorted_similar_property[i][0]
                        property_info = {
                            'property_id': int(filtered_property_df.iloc[index]['property_id']),
                            'property_title': filtered_property_df.iloc[index]['property_title'],
                            'price': str(filtered_property_df.iloc[index]['price']),
                            'name_location': filtered_property_df.iloc[index]['name_location'],
                            'latitude': filtered_property_df.iloc[index]['latitude'],
                            'longitude': filtered_property_df.iloc[index]['longitude'],
                            'price_value': filtered_property_df.iloc[index]['price_value'],
                            'total_area': filtered_property_df.iloc[index]['total_area'],
                            'possession': filtered_property_df.iloc[index]['possession'],
                            'status': filtered_property_df.iloc[index]['status'],
                            'transaction': filtered_property_df.iloc[index]['transaction'],
                            'furnish_type': filtered_property_df.iloc[index]['furnish_type']
                        }
                        recomms.append(property_info)
                    print(recomms)
                    for i in range(len(recomms)):
                        logger.info(recomms)
                    return recomms
            else:
                return jsonify([])

    else:
        return jsonify([])
