#!/usr/bin/env python3
"""
Environment Fix Script for CardioPredict
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_environment():
    """Fix Python environment issues"""
    print("🔧 Fixing Python environment...")
    
    # Uninstall problematic packages
    print("📦 Uninstalling old packages...")
    packages_to_remove = ["numpy", "pandas", "scikit-learn"]
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y")
    
    # Clear pip cache
    print("🧹 Clearing pip cache...")
    run_command("pip cache purge")
    
    # Install compatible versions
    print("📥 Installing compatible packages...")
    compatible_packages = [
        "numpy==1.26.4",
        "pandas==2.2.0", 
        "scikit-learn==1.4.0",
        "Flask==3.0.0",
        "Flask-CORS==4.0.0"
    ]
    
    for package in compatible_packages:
        success, out, err = run_command(f"pip install {package}")
        if success:
            print(f"✅ {package} installed")
        else:
            print(f"❌ Failed to install {package}: {err}")
    
    print("✅ Environment fix completed!")

if __name__ == "__main__":
    fix_environment()