# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkar_price_prediction_api = Flask("Superkart store Price Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_price_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkar_price_prediction_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Price Prediction API!"

# Define an endpoint for single food prediction (POST request)
@superkar_price_prediction_api.post('/v1/superkart')
def predict_price():
    """
    This function handles POST requests to the '/v1/superkart' endpoint.
    It expects a JSON payload containing food details and returns
    the predicted price as a JSON response.
    """
    # Get the JSON data from the request body
    food_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': food_data['Product_Weight'],
        'Product_Sugar_Content': food_data['Product_Sugar_Content'],
        'Product_Allocated_Area': food_data['Product_Allocated_Area'],
        'Product_MRP': food_data['Product_MRP'],
        'Store_Size': food_data['Store_Size'],
        'Store_Location_City_Type': food_data['Store_Location_City_Type'],
        'Store_Type': food_data['Store_Type'],
        'Product_Id_char': food_data['Product_Id_char'],
        'Store_Age_Years': food_data['Store_Age_Years'],
        'Product_Type_Category': food_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_price = model.predict(input_data)[0]

    # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)
    
    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})


# Define an endpoint for batch prediction (POST request)
@superkar_price_prediction_api.post('/v1/superkartbatch')
def predict_price_batch():
    """
    This function handles POST requests to the '/v1/superkartbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all food items in the DataFrame
    predicted_prices = model.predict(input_data).tolist()

    # Create a dictionary of predictions with IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the order of food items
    output_dict = dict(zip(property_ids, predicted_prices))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkar_price_prediction_api.run(debug=True)
