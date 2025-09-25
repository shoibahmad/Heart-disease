#!/usr/bin/env python3
"""
Test script for upgraded CardioPredict
"""

import sys
import numpy as np
import pandas as pd
import sklearn
import flask

print("Testing upgraded libraries...")
print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Flask: {flask.__version__}")

# Test model loading
try:
    from app import load_and_train_model
    model = load_and_train_model()
    if model:
        print("SUCCESS: Model loaded with upgraded libraries!")
    else:
        print("ERROR: Model failed to load")
except Exception as e:
    print(f"ERROR: {e}")