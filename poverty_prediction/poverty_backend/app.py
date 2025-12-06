from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
        
    # Check if model_data is a dictionary with 'model' key
    if isinstance(model_data, dict) and 'model' in model_data:
        model = model_data['model']
    else:
        # If it's a NumPy array, use it directly
        model = model_data
        
    print("✅ Model loaded successfully")
    print(f"Model type: {type(model).__name__}")
    
    # Print model info for debugging
    if hasattr(model, 'predict'):
        print("Model has predict method")
    else:
        print("Warning: Model does not have predict method")
        
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.get_json()
        
        # Debug print
        print("\nReceived data:", data)
        
        # Extract and convert features
        features = np.array([
            float(data['population']),           # Population
            float(data['average_income']),       # Average_Income_PHP
            float(data['unemployment_rate'])     # Unemployment_Rate
        ]).reshape(1, -1)

        # Debug prints
        print("\nInput features:", features)
        print("Feature types:", [type(x) for x in features[0]])
        print("Model type:", type(model))
        if hasattr(model, 'feature_importances_'):
            print("Feature importances:", model.feature_importances_)
        
        # Make prediction
        if hasattr(model, 'predict'):
            prediction = model.predict(features)[0]
            print("Raw prediction:", prediction)
            
            # Determine risk level
            if prediction >= 0.4:  # 40%
                risk_level = "Highest Risk Area"
            elif prediction >= 0.25:  # 25%
                risk_level = "High Risk Area"
            elif prediction >= 0.1:  # 10%
                risk_level = "Moderate Risk Area"
            else:
                risk_level = "Low Risk Area"
                
            return jsonify({
                'prediction': float(prediction * 100),  # Convert to percentage
                'risk_level': risk_level
            })
        else:
            return jsonify({'error': 'Model does not support prediction'}), 500
            
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
