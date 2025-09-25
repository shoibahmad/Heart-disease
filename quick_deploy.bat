@echo off
echo CardioPredict Quick Deploy
echo ============================

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Training model...
python train_model.py

echo Testing app...
python test_app.py

echo Starting Flask app...
echo Open your browser and go to: http://localhost:5000
python app.py

pause