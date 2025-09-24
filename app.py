from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

app = Flask(__name__)
CORS(app)

# Global model variable
model = None

def load_and_train_model():
    """Load data and train the model"""
    global model
    
    try:
        # Try to load pre-trained model first
        if os.path.exists('heart_disease_model.pkl'):
            with open('heart_disease_model.pkl', 'rb') as f:
                model = pickle.load(f)
            print("Pre-trained model loaded successfully")
            return model
        
        # If no pre-trained model, train new one
        heart_data = pd.read_csv('heart.csv')
        heart_data = heart_data.dropna()
        
        X = heart_data.drop(columns='target', axis=1)
        Y = heart_data['target']
        
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, Y_train)
        
        train_accuracy = accuracy_score(Y_train, model.predict(X_train))
        test_accuracy = accuracy_score(Y_test, model.predict(X_test))
        
        print(f"Model trained: Train={train_accuracy:.3f}, Test={test_accuracy:.3f}")
        
        # Save the model
        with open('heart_disease_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
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
        
        # Make prediction (no scaling needed for LogisticRegression)
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
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
    import os
    
    # Set secret key for sessions
    app.secret_key = os.environ.get('SECRET_KEY', 'cardiopredict_secret_key_2024')
    
    # Load and train the model on startup
    print("Loading and training model...")
    load_and_train_model()
    print("Model ready!")
    
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)