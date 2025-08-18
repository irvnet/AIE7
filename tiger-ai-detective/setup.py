#!/usr/bin/env python3
"""
Setup script for IBM Tiger Team Support System (using uv)
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_uv_installed():
    """Check if uv is installed"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up IBM Tiger Team Support System...")
    
    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Check if uv is installed
    if not check_uv_installed():
        print("❌ uv is not installed. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   or visit: https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)
    
    print("✅ uv detected")
    
    # Install dependencies using uv
    if not run_command("uv sync", "Installing dependencies with uv"):
        sys.exit(1)
    
    # Create database tables
    if not run_command("uv run python -c \"from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)\"", "Creating database tables"):
        sys.exit(1)
    
    # Generate mock data
    if not run_command("uv run python scripts/generate_mock_data.py", "Generating mock data"):
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: uv run python run_app.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Enter your OpenAI API key in the sidebar")
    print("4. Click 'Initialize System' to start")
    print("5. Create your first Tiger Team case!")
    print("\n🔧 Development commands:")
    print("  - Run tests: uv run pytest")
    print("  - Format code: uv run black app/")
    print("  - Sort imports: uv run isort app/")
    print("  - Lint code: uv run flake8 app/")

if __name__ == "__main__":
    main()
