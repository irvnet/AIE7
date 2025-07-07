#!/usr/bin/env python3
"""
Setup script for environment variables
"""

import os
from getpass import getpass

def setup_openai_key():
    """Securely set up OpenAI API key"""
    
    print("🔑 Setting up OpenAI API Key")
    print("=" * 30)
    
    # Check if key is already set
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY is already set")
        return True
    
    # Get API key securely
    api_key = getpass("Enter your OpenAI API key (input will be hidden): ")
    
    if not api_key or api_key.strip() == "":
        print("❌ No API key provided")
        return False
    
    # Set environment variable for current session
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Create .env file for future sessions
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ API key saved to .env file")
    except Exception as e:
        print(f"⚠️  Could not save to .env file: {e}")
        print("   The key is set for this session only")
    
    print("✅ OpenAI API key is now configured!")
    return True

def test_api_key():
    """Test if the API key is working"""
    
    print("\n🧪 Testing API key...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ No API key found")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI()
        
        # Test with a simple request
        response = client.models.list()
        print("✅ API key is valid and working!")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Environment Setup for RAG Pipeline")
    print("=" * 40)
    
    # Setup API key
    if setup_openai_key():
        # Test the key
        test_api_key()
    
    print("\n💡 Next steps:")
    print("   1. Your API key is now set for this session")
    print("   2. The .env file will be loaded automatically")
    print("   3. You can now run your RAG pipeline with PDF support!")
    print("   4. The .env file is in .gitignore for security") 