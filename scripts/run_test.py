#!/usr/bin/env python3
"""
WhatsApp-Driven Google Drive Assistant - Test Launcher
This script provides options to run the test in different modes.
"""

import sys
import os
import subprocess
import webbrowser
import time

def print_banner():
    print("=" * 60)
    print("🤖 WhatsApp-Driven Google Drive Assistant - Test Launcher")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are available"""
    missing = []
    
    # Check Python
    if sys.version_info < (3, 6):
        missing.append("Python 3.6+")
    
    # Check Flask for web interface
    try:
        import flask
    except ImportError:
        missing.append("Flask (pip install flask)")
    
    # Check tkinter for GUI
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (usually comes with Python)")
    
    return missing

def run_terminal_test():
    """Run the terminal-based test"""
    print("🚀 Starting terminal-based test...")
    script_path = os.path.join(os.path.dirname(__file__), "test_workflow.py")
    subprocess.run([sys.executable, script_path])

def run_web_test():
    """Run the web-based test"""
    print("🌐 Starting web-based test...")
    script_path = os.path.join(os.path.dirname(__file__), "test_workflow_web.py")
    
    # Start the web server
    process = subprocess.Popen([sys.executable, script_path])
    
    print("⏳ Starting web server...")
    time.sleep(2)
    
    # Open browser
    try:
        webbrowser.open("http://localhost:5000")
        print("✅ Web interface opened in your browser!")
        print("🌐 URL: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the web server")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping web server...")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print("🌐 Please manually open: http://localhost:5000")

def run_gui_test():
    """Run the GUI-based test"""
    print("🖥️  Starting GUI-based test...")
    script_path = os.path.join(os.path.dirname(__file__), "test_workflow_gui.py")
    subprocess.run([sys.executable, script_path])

def main():
    print_banner()
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print("⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("💡 To install Flask: pip install flask")
        print()
    
    while True:
        print("Choose your test mode:")
        print("1. 🖥️  Terminal Mode (Command line interface)")
        print("2. 🌐 Web Mode (Browser interface)")
        print("3. 🖥️  GUI Mode (Desktop application)")
        print("4. ❌ Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_terminal_test()
            break
        elif choice == "2":
            if "Flask" in missing_deps:
                print("❌ Flask is required for web mode. Please install it first:")
                print("   pip install flask")
                print()
                continue
            run_web_test()
            break
        elif choice == "3":
            if "tkinter" in missing_deps:
                print("❌ tkinter is required for GUI mode.")
                print("   It usually comes with Python installation.")
                print()
                continue
            run_gui_test()
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            print()

if __name__ == "__main__":
    main()
