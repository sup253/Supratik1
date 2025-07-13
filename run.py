#!/usr/bin/env python3
"""
Simple launcher script for the English Speaking Practice App
"""

import sys
import subprocess
import importlib.util

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🎯 English Speaking Practice App Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Required packages
    required_packages = [
        ("pyttsx3", "pyttsx3==2.90"),
        ("speech_recognition", "SpeechRecognition==3.10.0"),
        ("pyaudio", "pyaudio==0.2.11")
    ]
    
    # Check and install missing packages
    missing_packages = []
    for package_name, install_name in required_packages:
        if not check_package(package_name):
            missing_packages.append((package_name, install_name))
    
    if missing_packages:
        print(f"\n📦 Missing packages detected: {len(missing_packages)}")
        print("Attempting to install missing packages...")
        
        for package_name, install_name in missing_packages:
            print(f"Installing {package_name}...")
            if install_package(install_name):
                print(f"✅ {package_name} installed successfully")
            else:
                print(f"❌ Failed to install {package_name}")
                print(f"Please install manually: pip install {install_name}")
                
        # Re-check packages
        still_missing = []
        for package_name, install_name in required_packages:
            if not check_package(package_name):
                still_missing.append(package_name)
        
        if still_missing:
            print(f"\n❌ Still missing packages: {', '.join(still_missing)}")
            print("Please install them manually and try again.")
            sys.exit(1)
    
    print("✅ All required packages are installed")
    
    # Try to import and run the main application
    try:
        print("\n🚀 Starting English Speaking Practice App...")
        from english_speaking_app import main
        main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure english_speaking_app.py is in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if your microphone is working")
        print("2. Ensure you have internet connection")
        print("3. Try running: python english_speaking_app.py directly")
        sys.exit(1)

if __name__ == "__main__":
    main()