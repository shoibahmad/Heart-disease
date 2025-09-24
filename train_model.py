#!/usr/bin/env python3
"""
Heart Disease Model Training Script
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

def train_heart_disease_model():
    """Train and save the heart disease prediction model"""
    
    # Load data
    try:
        heart_data = pd.read_csv('heart.csv')
        print(f"Data loaded successfully: {heart_data.shape}")
    except FileNotFoundError:
        print("Error: heart.csv not found!")
        return False
    
    # Prepare features and target
    X = heart_data.drop(columns='target', axis=1)
    Y = heart_data['target']
    
    # Split data
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, stratify=Y, random_state=2
    )
    
    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, Y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_accuracy = accuracy_score(Y_train, train_pred)
    test_accuracy = accuracy_score(Y_test, test_pred)
    
    print(f"Training Accuracy: {train_accuracy:.3f}")
    print(f"Test Accuracy: {test_accuracy:.3f}")
    
    # Save model
    with open('heart_disease_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model saved as heart_disease_model.pkl")
    return True

if __name__ == "__main__":
    print("Training Heart Disease Prediction Model...")
    success = train_heart_disease_model()
    
    if success:
        print("Model training completed successfully!")
    else:
        print("Model training failed!")