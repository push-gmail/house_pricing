from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can access backend

# Load the trained model
model = joblib.load('HousePrediction.joblib')

# 👋 Home route to confirm server is running
@app.route('/')
def home():
    return '✅ House Price Prediction API is Running!'

# 📡 Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        avg_area = float(data['avg_area'])
        income = float(data['income'])
        rooms = float(data['rooms'])
        bedrooms = float(data['bedrooms'])
        population = float(data['population'])

        prediction = model.predict([[avg_area, income, rooms,bedrooms, population]])
        return jsonify({'predicted_price': round(prediction[0], 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 🚀 Run the app
if __name__ == '__main__':
    print("🚀 Flask API is starting...")
    app.run(debug=True)

