#!/usr/bin/env python3
"""
Test script for API key manager
"""

from api_key_manager import APIKeys, validate_api_keys, get_api_keys

def test_api_key_validation():
    """Test API key validation"""
    print("🧪 Testing API Key Validation")
    print("=" * 40)
    
    # Test valid keys
    valid_keys = APIKeys(
        openai_api_key="sk-test1234567890abcdef",
        tavily_api_key="tav-test1234567890",
        langsmith_api_key="lsv2_test1234567890abcdef"
    )
    
    errors = validate_api_keys(valid_keys)
    if not errors:
        print("✅ Valid keys passed validation")
    else:
        print(f"❌ Valid keys failed validation: {errors}")
    
    # Test invalid keys
    invalid_keys = APIKeys(
        openai_api_key="invalid-key",
        tavily_api_key="short",
        langsmith_api_key="invalid-langsmith-key"
    )
    
    errors = validate_api_keys(invalid_keys)
    if errors:
        print("✅ Invalid keys correctly caught:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("❌ Invalid keys should have been caught")
    
    # Test missing required key
    missing_keys = APIKeys(
        openai_api_key="",  # Empty required key
        tavily_api_key=None,
        langsmith_api_key=None
    )
    
    errors = validate_api_keys(missing_keys)
    if errors:
        print("✅ Missing required key correctly caught:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("❌ Missing required key should have been caught")

def test_environment_variables():
    """Test environment variable handling"""
    print("\n🧪 Testing Environment Variable Handling")
    print("=" * 40)
    
    # Set test environment variables
    import os
    os.environ["OPENAI_API_KEY"] = "sk-test-from-env"
    os.environ["TAVILY_API_KEY"] = "tav-test-from-env"
    os.environ["LANGCHAIN_API_KEY"] = "lsv2_test-from-env"
    
    print("✅ Environment variables set for testing")
    
    # Test that they're detected
    keys = get_api_keys(interactive=False)
    print(f"✅ Retrieved keys from environment:")
    print(f"  - OpenAI: {keys.openai_api_key[:10]}...")
    print(f"  - Tavily: {keys.tavily_api_key[:10]}...")
    print(f"  - LangSmith: {keys.langsmith_api_key[:10]}...")

if __name__ == "__main__":
    test_api_key_validation()
    test_environment_variables()
    print("\n✅ API Key Manager tests completed!") 