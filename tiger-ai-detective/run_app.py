#!/usr/bin/env python3
"""
Launcher script for IBM Tiger Team Support System (using uv)
"""

import subprocess
import sys
import os

def check_uv_installed():
    """Check if uv is installed"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Launch the Streamlit application"""
    print("🚀 Starting IBM Tiger Team Support System...")
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: app/main.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if uv is installed
    if not check_uv_installed():
        print("❌ Error: uv is not installed. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Run the Streamlit app using uv
    try:
        subprocess.run([
            "uv", "run", "python", "-m", "streamlit", "run", "app/main.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
