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

def deploy_railway():
    """Deploy to Railway"""
    print("🚂 Deploying to Railway...")
    print("1. Go to railway.app")
    print("2. Connect your GitHub repository")
    print("3. Click Deploy")
    print("✅ Railway will auto-detect and deploy your Flask app!")

def deploy_render():
    """Deploy to Render"""
    print("🎨 Deploying to Render...")
    print("1. Go to render.com")
    print("2. Connect GitHub repository")
    print("3. Create Web Service with:")
    print("   - Build: pip install -r requirements.txt")
    print("   - Start: python app.py")
    print("✅ Render will deploy your app for free!")

def deploy_local():
    """Run locally for testing"""
    print("🏠 Running locally...")
    print("Installing dependencies...")
    run_command("pip install --upgrade pip")
    run_command("pip install -r requirements.txt")
    
    os.environ['FLASK_ENV'] = 'development'
    print("✅ Starting Flask app...")
    print("🌐 Open: http://localhost:5000")
    os.system("python app.py")

def main():
    print("🚀 CardioPredict Deployment Tool")
    print("=" * 35)
    print("1. 🔥 Deploy to Heroku (5 min)")
    print("2. 🚂 Deploy to Railway (2 min)")
    print("3. 🎨 Deploy to Render (3 min)")
    print("4. 🏠 Run locally")
    print("5. ❌ Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        deploy_heroku()
    elif choice == "2":
        deploy_railway()
    elif choice == "3":
        deploy_render()
    elif choice == "4":
        deploy_local()
    elif choice == "5":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice!")
        main()

if __name__ == "__main__":
    main()