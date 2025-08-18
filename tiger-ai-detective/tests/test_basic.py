#!/usr/bin/env python3
"""
Basic tests for IBM Tiger Team Support System
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import engine, SessionLocal
from app.models.schemas import Base, Customer, Product, TigerTeamMember, Case

def test_database_connection():
    """Test that we can connect to the database"""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        assert True, "Database connection successful"
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_customer_model():
    """Test customer model creation"""
    try:
        customer = Customer(
            name="Test Customer",
            company="Test Company",
            industry="Technology",
            region="North America",
            contact_email="test@example.com",
            contact_phone="555-1234"
        )
        
        assert customer.name == "Test Customer"
        assert customer.company == "Test Company"
        assert customer.industry == "Technology"
        
    except Exception as e:
        pytest.fail(f"Customer model test failed: {e}")

def test_product_model():
    """Test product model creation"""
    try:
        product = Product(
            name="IBM WebSphere Application Server",
            category="Application Server",
            version="9.0.5",
            description="Enterprise Java application server",
            documentation_url="https://www.ibm.com/docs/en/was/9.0.5"
        )
        
        assert product.name == "IBM WebSphere Application Server"
        assert product.category == "Application Server"
        assert product.version == "9.0.5"
        
    except Exception as e:
        pytest.fail(f"Product model test failed: {e}")

def test_tiger_team_member_model():
    """Test Tiger Team member model creation"""
    try:
        member = TigerTeamMember(
            name="John Doe",
            email="john.doe@ibm.com",
            expertise_areas=["Application Server", "Database"],
            experience_years=10,
            is_available=True,
            current_case_count=2
        )
        
        assert member.name == "John Doe"
        assert member.email == "john.doe@ibm.com"
        assert member.expertise_areas == ["Application Server", "Database"]
        assert member.experience_years == 10
        assert member.is_available == True
        
    except Exception as e:
        pytest.fail(f"Tiger Team member model test failed: {e}")

def test_case_model():
    """Test case model creation"""
    try:
        case = Case(
            case_number="TT20241201001",
            support_ticket_id=1,
            customer_id=1,
            product_id=1,
            assigned_member_id=1,
            title="Test Case",
            description="This is a test case",
            desired_outcome="Resolve the issue",
            priority="High",
            status="Open"
        )
        
        assert case.case_number == "TT20241201001"
        assert case.title == "Test Case"
        assert case.priority == "High"
        assert case.status == "Open"
        
    except Exception as e:
        pytest.fail(f"Case model test failed: {e}")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
