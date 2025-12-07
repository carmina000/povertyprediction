from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os
import numpy as np
from pathlib import Path

# Initialize Flask app
app = Flask(__name__, static_folder=None)  # We'll set this dynamically
CORS(app)

# Load your model
model = None
try:
    model_path = os.path.join(Path(__file__).parent.parent, 'random_forest_model.pkl')
    model = pickle.load(open(model_path, 'rb'))
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Serve frontend files in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API endpoint
@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "preflight"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        return response

    try:
        data = request.get_json()
        print("Received data:", data)
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Expected features
        expected_features = {
            'Population': float,
            'Average_Income_PHP': float,
            'Unemployment_Rate': float
        }
        
        # Validate and extract features
        features = {}
        for feature, feature_type in expected_features.items():
            if feature not in data:
                return jsonify({
                    "error": f"Missing required feature: {feature}",
                    "required_features": list(expected_features.keys())
                }), 400
            try:
                features[feature] = feature_type(data[feature])
            except (ValueError, TypeError):
                return jsonify({
                    "error": f"Invalid format for {feature}. Expected {feature_type.__name__}."
                }), 400

        # Make prediction
        feature_values = [features[feature] for feature in expected_features.keys()]
        features_array = np.array(feature_values).reshape(1, -1)
        prediction = model.predict(features_array)[0]

        return jsonify({
            "prediction": float(prediction),
            "status": "success",
            "input_features": features
        })
        
    except Exception as e:
        return jsonify({
            "error": "An error occurred during prediction",
            "details": str(e)
        }), 500

# For local development
if __name__ == '__main__':
    app.static_folder = os.path.join(Path(__file__).parent.parent.parent, 'poverty-frontend', 'dist')
    app.run(host='0.0.0.0', port=5001, debug=True)