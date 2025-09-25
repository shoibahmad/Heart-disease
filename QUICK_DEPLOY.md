# 🚀 Quick Deploy CardioPredict

## Method 1: Heroku (Easiest - 5 minutes)

### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Initialize git (if not done)
git init
git add .
git commit -m "Deploy CardioPredict"

# Create and deploy
heroku create your-app-name
git push heroku main

# Your app is live at: https://your-app-name.herokuapp.com
```

## Method 2: Railway (Fastest - 2 minutes)

### Step 1: Go to railway.app
### Step 2: Connect GitHub repository
### Step 3: Deploy automatically

## Method 3: Render (Free Forever)

### Step 1: Go to render.com
### Step 2: Connect GitHub
### Step 3: Use Web Service with:
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

## Method 4: PythonAnywhere (Free Tier)

### Step 1: Upload files to pythonanywhere.com
### Step 2: Create web app with Flask
### Step 3: Configure WSGI file

## One-Click Deploy Options

### Heroku Button
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Railway Button
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Local Testing
```bash
python app.py
# Visit: http://localhost:5000
```