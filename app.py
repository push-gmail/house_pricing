from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import certifi
from pymongo import MongoClient
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('HousePrediction.joblib')

# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://agarwalsurbhi1610:suRprO%40709@ml-cluster.tl8llhr.mongodb.net/ml_project?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = client['ml_project']  # Database name
collection = db['predictions']  # Collection name

# 👋 Home route
@app.route('/')
def home():
    return '✅ House Price Prediction API with MongoDB is Running!'

# 📡 Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        # Extract input features
        avg_area = float(data['avg_area'])
        income = float(data['income'])
        rooms = float(data['rooms'])
        bedrooms = float(data['bedrooms'])
        population = float(data['population'])

        # Make prediction
        prediction = model.predict([[avg_area, income, rooms, bedrooms, population]])[0]

        # Save to MongoDB
        record = {
            'avg_area': avg_area,
            'income': income,
            'rooms': rooms,
            'bedrooms': bedrooms,
            'population': population,
            'predicted_price': round(prediction, 2),
            'timestamp': datetime.now()
        }
        collection.insert_one(record)

        # Return prediction
        return jsonify({'predicted_price': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 🚀 Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
