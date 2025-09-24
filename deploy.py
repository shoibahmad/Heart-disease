#!/usr/bin/env python3
"""
Quick deployment script for CardioPredict
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def deploy_heroku():
    """Deploy to Heroku"""
    print("Deploying to Heroku...")
    
    # Check if git repo exists
    if not os.path.exists('.git'):
        print("Initializing git repository...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
    
    # Create Heroku app
    app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
    if app_name:
        success, out, err = run_command(f"heroku create {app_name}")
    else:
        success, out, err = run_command("heroku create")
    
    if not success:
        print(f"Failed to create Heroku app: {err}")
        return False
    
    # Set environment variables
    run_command("heroku config:set FLASK_ENV=production")
    run_command("heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')")
    
    # Deploy
    print("Deploying to Heroku...")
    success, out, err = run_command("git push heroku main")
    
    if success:
        print("Successfully deployed to Heroku!")
        run_command("heroku open")
        return True
    else:
        print(f"Deployment failed: {err}")
        return False

def deploy_local():
    """Run locally for testing"""
    print("Running locally...")
    
    # First, reinstall dependencies
    print("Installing dependencies...")
    success, out, err = run_command("pip install --only-binary=all numpy pandas scikit-learn Flask Flask-CORS")
    if not success:
        print(f"Warning: {err}")
    
    # Train model if needed
    print("Training model...")
    success, out, err = run_command("python train_model.py")
    if not success:
        print(f"Model training warning: {err}")
    
    # Test the app
    print("Testing app...")
    success, out, err = run_command("python test_app.py")
    if success:
        print("App test passed!")
    else:
        print(f"App test failed: {err}")
        return
    
    # Run the app
    os.environ['FLASK_ENV'] = 'development'
    print("Starting Flask app...")
    print("Open your browser and go to: http://localhost:5000")
    os.system("python app.py")

def main():
    print("CardioPredict Deployment Tool")
    print("=" * 30)
    print("1. Deploy to Heroku")
    print("2. Run locally")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        deploy_heroku()
    elif choice == "2":
        deploy_local()
    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice!")
        main()

if __name__ == "__main__":
    main()