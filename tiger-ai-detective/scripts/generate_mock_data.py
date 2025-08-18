#!/usr/bin/env python3
"""
Mock Data Generator for IBM Tiger Team Support System
Generates realistic data for IBM products, customers, support tickets, and Tiger Team members.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models.schemas import Base, Customer, Product, TigerTeamMember, SupportTicket, Case, Evidence
import random
from datetime import datetime, timedelta
import uuid

# Initialize Faker
fake = Faker()

# IBM Products Data
IBM_PRODUCTS = [
    {
        "name": "IBM WebSphere Application Server",
        "category": "Application Server",
        "version": "9.0.5",
        "description": "Enterprise Java application server for building, deploying, and managing applications",
        "documentation_url": "https://www.ibm.com/docs/en/was/9.0.5"
    },
    {
        "name": "IBM Db2 Database",
        "category": "Database",
        "version": "11.5",
        "description": "Enterprise database management system with advanced analytics capabilities",
        "documentation_url": "https://www.ibm.com/docs/en/db2/11.5"
    },
    {
        "name": "IBM MQ",
        "category": "Messaging",
        "version": "9.3",
        "description": "Enterprise messaging middleware for reliable application integration",
        "documentation_url": "https://www.ibm.com/docs/en/ibm-mq/9.3"
    },
    {
        "name": "IBM Cloud Pak for Data",
        "category": "Cloud Platform",
        "version": "4.7",
        "description": "Integrated data and AI platform for building and deploying AI applications",
        "documentation_url": "https://www.ibm.com/docs/en/cloud-pak-data/4.7"
    },
    {
        "name": "IBM Watson Assistant",
        "category": "AI Services",
        "version": "2.0",
        "description": "AI-powered virtual assistant for building conversational interfaces",
        "documentation_url": "https://www.ibm.com/docs/en/watson-assistant/2.0"
    },
    {
        "name": "IBM Cognos Analytics",
        "category": "Business Intelligence",
        "version": "11.2",
        "description": "Business intelligence and performance management software",
        "documentation_url": "https://www.ibm.com/docs/en/cognos-analytics/11.2"
    },
    {
        "name": "IBM Sterling B2B Integrator",
        "category": "Integration",
        "version": "6.1",
        "description": "B2B integration platform for managing trading partner relationships",
        "documentation_url": "https://www.ibm.com/docs/en/sterling-b2b-integrator/6.1"
    },
    {
        "name": "IBM Tivoli Storage Manager",
        "category": "Storage Management",
        "version": "8.1",
        "description": "Enterprise backup and recovery solution",
        "documentation_url": "https://www.ibm.com/docs/en/tsm/8.1"
    }
]

# Common Support Issues
SUPPORT_ISSUES = [
    "Performance degradation under high load",
    "Memory leaks causing system instability",
    "Database connection pool exhaustion",
    "SSL/TLS certificate validation failures",
    "Cluster node communication failures",
    "Backup and recovery failures",
    "Integration endpoint authentication issues",
    "Log file corruption and rotation problems",
    "Configuration synchronization issues",
    "Security vulnerability remediation",
    "High CPU utilization during peak hours",
    "Network connectivity issues between components",
    "Data corruption in transaction logs",
    "Application deployment failures",
    "License validation and renewal problems"
]

# Evidence Types
EVIDENCE_TYPES = [
    "System Logs",
    "Error Messages",
    "Performance Metrics",
    "Screenshots",
    "Configuration Files",
    "Network Traces",
    "Database Dumps",
    "Stack Traces",
    "Memory Dumps",
    "Application Logs"
]

def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def generate_customers(db: Session, count: int = 50):
    """Generate mock customers"""
    customers = []
    industries = ["Financial Services", "Healthcare", "Retail", "Manufacturing", "Technology", "Government", "Education"]
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
    
    for i in range(count):
        customer = Customer(
            name=fake.name(),
            company=fake.company(),
            industry=random.choice(industries),
            region=random.choice(regions),
            contact_email=fake.email(),
            contact_phone=fake.phone_number()
        )
        db.add(customer)
        customers.append(customer)
    
    db.commit()
    return customers

def generate_products(db: Session):
    """Generate IBM products"""
    products = []
    for product_data in IBM_PRODUCTS:
        product = Product(**product_data)
        db.add(product)
        products.append(product)
    
    db.commit()
    return products

def generate_tiger_team_members(db: Session, count: int = 15):
    """Generate Tiger Team members"""
    members = []
    expertise_areas = [
        ["Application Server", "Database"],
        ["Cloud Platform", "AI Services"],
        ["Messaging", "Integration"],
        ["Business Intelligence", "Storage Management"],
        ["Database", "Performance Tuning"],
        ["Security", "Application Server"],
        ["Cloud Platform", "Messaging"],
        ["AI Services", "Business Intelligence"],
        ["Integration", "Storage Management"],
        ["Performance Tuning", "Security"],
        ["Application Server", "Cloud Platform"],
        ["Database", "Messaging"],
        ["Business Intelligence", "Integration"],
        ["Storage Management", "AI Services"],
        ["Security", "Performance Tuning"]
    ]
    
    for i in range(count):
        member = TigerTeamMember(
            name=fake.name(),
            email=fake.email(),
            expertise_areas=expertise_areas[i] if i < len(expertise_areas) else ["Application Server"],
            experience_years=random.randint(5, 20),
            is_available=random.choice([True, True, True, False]),  # 75% available
            current_case_count=random.randint(0, 3)
        )
        db.add(member)
        members.append(member)
    
    db.commit()
    return members

def generate_support_tickets(db: Session, customers, products, count: int = 200):
    """Generate support tickets"""
    tickets = []
    severities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    
    for i in range(count):
        # Generate unique ticket number
        ticket_number = f"PMR{random.randint(100000, 999999)}"
        
        ticket = SupportTicket(
            ticket_number=ticket_number,
            customer_id=random.choice(customers).id,
            product_id=random.choice(products).id,
            title=random.choice(SUPPORT_ISSUES),
            description=fake.text(max_nb_chars=500),
            severity=random.choice(severities),
            status=random.choice(statuses),
            created_at=fake.date_time_between(start_date='-180d', end_date='now', tzinfo=None)
        )
        db.add(ticket)
        tickets.append(ticket)
    
    db.commit()
    return tickets

def generate_cases(db: Session, tickets, customers, products, members, count: int = 30):
    """Generate Tiger Team cases"""
    cases = []
    priorities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Open", "Research", "Customer Call", "Resolved"]
    
    for i in range(count):
        # Generate unique case number
        case_number = f"TT{random.randint(10000, 99999)}"
        
        # Select available member
        available_members = [m for m in members if m.is_available and m.current_case_count < 5]
        if not available_members:
            available_members = members
        
        assigned_member = random.choice(available_members)
        
        case = Case(
            case_number=case_number,
            support_ticket_id=random.choice(tickets).id,
            customer_id=random.choice(customers).id,
            product_id=random.choice(products).id,
            assigned_member_id=assigned_member.id,
            title=f"Tiger Team Case: {random.choice(SUPPORT_ISSUES)}",
            description=fake.text(max_nb_chars=1000),
            desired_outcome=fake.text(max_nb_chars=300),
            priority=random.choice(priorities),
            status=random.choice(statuses),
            research_notes=fake.text(max_nb_chars=800) if random.choice([True, False]) else None,
            ai_recommendations=fake.text(max_nb_chars=600) if random.choice([True, False]) else None,
            created_at=fake.date_time_between(start_date='-60d', end_date='now', tzinfo=None)
        )
        
        # Set first customer call date for some cases
        if case.status in ["Customer Call", "Resolved"]:
            case.first_customer_call_date = case.created_at + timedelta(days=random.randint(1, 5))
        
        db.add(case)
        cases.append(case)
        
        # Update member case count
        assigned_member.current_case_count += 1
    
    db.commit()
    return cases

def generate_evidence(db: Session, cases, count: int = 100):
    """Generate evidence for cases"""
    evidence_list = []
    
    for i in range(count):
        case = random.choice(cases)
        evidence = Evidence(
            case_id=case.id,
            evidence_type=random.choice(EVIDENCE_TYPES),
            content=fake.text(max_nb_chars=400),
            source=fake.company(),
            relevance_score=random.randint(1, 10),
            created_at=fake.date_time_between(start_date='-30d', end_date='now', tzinfo=None)
        )
        db.add(evidence)
        evidence_list.append(evidence)
    
    db.commit()
    return evidence_list

def main():
    """Main function to generate all mock data"""
    print("🚀 Generating mock data for IBM Tiger Team Support System...")
    
    # Create database tables
    create_database()
    print("✅ Database tables created")
    
    db = SessionLocal()
    try:
        # Generate data
        print("👥 Generating customers...")
        customers = generate_customers(db, 50)
        print(f"✅ Generated {len(customers)} customers")
        
        print("📦 Generating IBM products...")
        products = generate_products(db)
        print(f"✅ Generated {len(products)} products")
        
        print("🦁 Generating Tiger Team members...")
        members = generate_tiger_team_members(db, 15)
        print(f"✅ Generated {len(members)} Tiger Team members")
        
        print("🎫 Generating support tickets...")
        tickets = generate_support_tickets(db, customers, products, 200)
        print(f"✅ Generated {len(tickets)} support tickets")
        
        print("📋 Generating Tiger Team cases...")
        cases = generate_cases(db, tickets, customers, products, members, 30)
        print(f"✅ Generated {len(cases)} cases")
        
        print("🔍 Generating evidence...")
        evidence = generate_evidence(db, cases, 100)
        print(f"✅ Generated {len(evidence)} evidence items")
        
        print("\n🎉 Mock data generation completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Customers: {len(customers)}")
        print(f"   - Products: {len(products)}")
        print(f"   - Tiger Team Members: {len(members)}")
        print(f"   - Support Tickets: {len(tickets)}")
        print(f"   - Cases: {len(cases)}")
        print(f"   - Evidence Items: {len(evidence)}")
        
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
