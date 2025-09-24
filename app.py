from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle
import os

app = Flask(__name__)
CORS(app)

# Global model and scaler variables
model = None
scaler = None

def load_and_train_model():
    """Load data and train the model with improved accuracy"""
    global model, scaler
    
    try:
        # Load the heart disease dataset
        heart_data = pd.read_csv('heart.csv')
        
        # Remove any incomplete rows
        heart_data = heart_data.dropna()
        
        # Prepare features and target
        X = heart_data.drop(columns='target', axis=1)
        Y = heart_data['target']
        
        # Split the data
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42)
        
        # Scale the features for better performance
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train the model with Random Forest for better accuracy
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train_scaled, Y_train)
        
        # Calculate accuracy
        train_accuracy = accuracy_score(Y_train, model.predict(X_train_scaled))
        test_accuracy = accuracy_score(Y_test, model.predict(X_test_scaled))
        
        print(f"Model trained successfully with {len(heart_data)} samples")
        print(f"Training accuracy: {train_accuracy:.3f}")
        print(f"Testing accuracy: {test_accuracy:.3f}")
        return model
        
    except Exception as e:
        print(f"Error loading/training model: {e}")
        raise e

@app.route('/')
def index():
    """Serve the patient name entry page"""
    return render_template('patient_name.html')

@app.route('/assessment')
def assessment():
    """Serve the assessment form"""
    patient_name = session.get('patient_name', 'Unknown Patient')
    return render_template('assessment.html', patient_name=patient_name)

@app.route('/set_patient', methods=['POST'])
def set_patient():
    """Set patient name in session"""
    data = request.get_json()
    session['patient_name'] = data.get('patient_name', 'Unknown Patient')
    return jsonify({'success': True})

@app.route('/predict', methods=['POST'])
def predict():
    """Predict heart disease based on input parameters"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract features
        features = [
            float(data['age']),
            int(data['sex']),
            int(data['cp']),
            float(data['trestbps']),
            float(data['chol']),
            int(data['fbs']),
            int(data['restecg']),
            float(data['thalach']),
            int(data['exang']),
            float(data['oldpeak']),
            int(data['slope']),
            int(data['ca']),
            int(data['thal'])
        ]
        
        # Create DataFrame with feature names
        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        input_df = pd.DataFrame([features], columns=feature_names)
        
        # Scale the input features
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        
        # Determine risk level
        if probability >= 0.7:
            risk_level = "High"
            risk_color = "#dc3545"
        elif probability >= 0.4:
            risk_level = "Moderate"
            risk_color = "#ffc107"
        else:
            risk_level = "Low"
            risk_color = "#28a745"
        
        # Store patient data and results in session
        session['patient_data'] = data
        session['prediction_results'] = {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'message': 'Heart disease detected' if prediction == 1 else 'No heart disease detected'
        }
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'message': 'Heart disease detected' if prediction == 1 else 'No heart disease detected'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/results')
def results():
    """Show detailed results page"""
    patient_name = session.get('patient_name', 'Unknown Patient')
    patient_data = session.get('patient_data', {})
    prediction_results = session.get('prediction_results', {})
    
    return render_template('results.html', 
                         patient_name=patient_name,
                         patient_data=patient_data,
                         prediction_results=prediction_results)

if __name__ == '__main__':
    # Set secret key for sessions
    app.secret_key = 'cardiopredict_secret_key_2024'
    
    # Load and train the model on startup
    print("Loading and training model...")
    load_and_train_model()
    print("Model ready!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)