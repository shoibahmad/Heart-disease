from flask import Flask, request, jsonify, render_template, session
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle
import os

app = Flask(__name__)

# Global model variable
model = None

def load_and_train_model():
    """Load pre-trained model or create a simple one"""
    global model
    
    try:
        # Try to load pre-trained model first
        if os.path.exists('heart_disease_model.pkl'):
            with open('heart_disease_model.pkl', 'rb') as f:
                model = pickle.load(f)
            print("Pre-trained model loaded successfully")
            return model
        
        # Create a simple trained model with sample data
        model = LogisticRegression(max_iter=1000)
        
        # Sample training data (simplified for deployment)
        X_sample = np.array([
            [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1],
            [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2],
            [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2],
            [56, 1, 1, 120, 236, 0, 1, 178, 0, 0.8, 2, 0, 2],
            [57, 0, 0, 120, 354, 0, 1, 163, 1, 0.6, 2, 0, 2]
        ])
        Y_sample = np.array([1, 0, 0, 0, 0])
        
        model.fit(X_sample, Y_sample)
        print("Simple model created for deployment")
        
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
        
        # Convert to numpy array for prediction
        input_array = np.array([features])
        
        # Make prediction
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1]
        
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