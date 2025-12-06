import pickle
import os
from flask import Flask
app = Flask(__name__)

def check_model(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
            
        # Get file info
        file_size = os.path.getsize(file_path) / 1024  # in KB
        print(f"📄 File: {file_path}")
        print(f"📊 Size: {file_size:.2f} KB")
        print(f"📅 Last modified: {os.path.getmtime(file_path)}")
        
        # Try to load the model
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
            
        print("\n✅ This appears to be a valid pickle file.")
        print(f"📝 Object type: {type(model).__name__}")
        
        # Check if it's a scikit-learn model
        if hasattr(model, 'predict'):
            print("🎯 This is a trained scikit-learn model!")
            print(f"Model class: {model.__class__.__name__}")
            
            # Get more model info if available
            if hasattr(model, 'n_estimators'):
                print(f"Number of trees: {model.n_estimators}")
            if hasattr(model, 'feature_importances_'):
                print(f"Number of features: {len(model.feature_importances_)}")
                
        elif isinstance(model, dict):
            print("📚 This is a dictionary containing:")
            for key in model.keys():
                print(f"- {key}: {type(model[key]).__name__}")
                if hasattr(model[key], 'predict'):
                    print(f"  🎯 Found a model: {model[key].__class__.__name__}")
        
    except Exception as e:
        print(f"\n❌ Error loading the model: {e}")

if __name__ == "__main__":
    model_path = r"C:\Users\ACER\OneDrive\Documents\.newpovertyprediction\random_forest_model.pkl"
    check_model(model_path)
