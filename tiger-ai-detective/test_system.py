#!/usr/bin/env python3
"""
System test for IBM Tiger Team Support System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    print("🔄 Testing imports...")
    
    try:
        from app.models.database import engine, SessionLocal, Base
        from app.models.schemas import Customer, Product, TigerTeamMember, Case, Evidence
        print("✅ Database models imported successfully")
    except ImportError as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_openai.embeddings import OpenAIEmbeddings
        print("✅ LangChain imports successful")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and table creation"""
    print("🔄 Testing database...")
    
    try:
        from app.models.database import engine, Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_models():
    """Test model creation"""
    print("🔄 Testing models...")
    
    try:
        from app.models.schemas import Customer, Product, TigerTeamMember, Case
        
        # Test customer model
        customer = Customer(
            name="Test Customer",
            company="Test Company",
            industry="Technology"
        )
        print("✅ Customer model created")
        
        # Test product model
        product = Product(
            name="IBM WebSphere",
            category="Application Server",
            version="9.0.5"
        )
        print("✅ Product model created")
        
        # Test Tiger Team member model
        member = TigerTeamMember(
            name="John Doe",
            email="john@ibm.com",
            expertise_areas=["Application Server"]
        )
        print("✅ Tiger Team member model created")
        
        # Test case model
        case = Case(
            case_number="TT20241201001",
            title="Test Case",
            description="Test description",
            priority="High"
        )
        print("✅ Case model created")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🧪 Running IBM Tiger Team Support System Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Test", test_database),
        ("Model Test", test_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 Next steps:")
        print("1. Run: uv run python run_app.py")
        print("2. Open: http://localhost:8501")
        print("3. Enter your OpenAI API key")
        print("4. Click 'Initialize System'")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
