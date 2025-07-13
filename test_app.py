#!/usr/bin/env python3
"""
Test script for the English Speaking Practice App
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
        
        try:
            import speech_recognition as sr
            print("✅ speech_recognition imported successfully")
            speech_available = True
        except ImportError:
            print("⚠️  speech_recognition not available - using fallback mode")
            speech_available = False
            
        return True, speech_available
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False, False

def test_tts():
    """Test text-to-speech functionality"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        print("✅ Text-to-speech engine initialized successfully")
        return True
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def main():
    print("🎯 English Speaking Practice App - Component Test")
    print("=" * 50)
    
    # Test imports
    imports_ok, speech_available = test_imports()
    if not imports_ok:
        print("\n❌ Critical imports failed!")
        sys.exit(1)
    
    # Test TTS
    tts_ok = test_tts()
    if not tts_ok:
        print("\n❌ Text-to-speech test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed!")
    print("\nApplication Status:")
    print(f"  • Text-to-speech: ✅ Available")
    print(f"  • Speech recognition: {'✅ Available' if speech_available else '⚠️ Disabled (fallback mode)'}")
    print(f"  • GUI framework: ✅ Available")
    
    print("\nYou can now run the application with:")
    print("  python english_speaking_app.py")
    print("  or")
    print("  python run.py")
    
    if not speech_available:
        print("\n📝 Note: Speech recognition is disabled due to compatibility issues.")
        print("   The app will work in practice mode where you can:")
        print("   - Listen to pronunciations")
        print("   - Practice speaking aloud")
        print("   - Mark exercises as completed")
        print("   - Track your progress")

if __name__ == "__main__":
    main()