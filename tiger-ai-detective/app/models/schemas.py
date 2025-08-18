from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# SQLAlchemy Models
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    industry = Column(String(100))
    region = Column(String(100))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    support_tickets = relationship("SupportTicket", back_populates="customer")
    cases = relationship("Case", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))  # e.g., "Application Server", "Database", "Cloud"
    version = Column(String(50))
    description = Column(Text)
    documentation_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    support_tickets = relationship("SupportTicket", back_populates="product")
    cases = relationship("Case", back_populates="product")

class TigerTeamMember(Base):
    __tablename__ = "tiger_team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    expertise_areas = Column(JSON)  # List of product categories
    experience_years = Column(Integer)
    is_available = Column(Boolean, default=True)
    current_case_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    assigned_cases = relationship("Case", back_populates="assigned_member")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    title = Column(String(500), nullable=False)
    description = Column(Text)
    severity = Column(String(20))  # Critical, High, Medium, Low
    status = Column(String(50))  # Open, In Progress, Resolved, Closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="support_tickets")
    product = relationship("Product", back_populates="support_tickets")
    cases = relationship("Case", back_populates="support_ticket")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), nullable=False, unique=True)
    support_ticket_id = Column(Integer, ForeignKey("support_tickets.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    assigned_member_id = Column(Integer, ForeignKey("tiger_team_members.id"))
    
    title = Column(String(500), nullable=False)
    description = Column(Text)
    desired_outcome = Column(Text)
    priority = Column(String(20))  # Critical, High, Medium, Low
    status = Column(String(50), default="Open")  # Open, Research, Customer Call, Resolved
    research_notes = Column(Text)
    ai_recommendations = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    first_customer_call_date = Column(DateTime(timezone=True))
    
    # Relationships
    support_ticket = relationship("SupportTicket", back_populates="cases")
    customer = relationship("Customer", back_populates="cases")
    product = relationship("Product", back_populates="cases")
    assigned_member = relationship("TigerTeamMember", back_populates="assigned_cases")
    evidence = relationship("Evidence", back_populates="case")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    evidence_type = Column(String(50))  # Logs, Screenshots, Error Messages, etc.
    content = Column(Text)
    source = Column(String(255))  # Where this evidence came from
    relevance_score = Column(Integer)  # AI-generated relevance score
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="evidence")

# Pydantic Models for API
class CustomerCreate(BaseModel):
    name: str
    company: str
    industry: Optional[str] = None
    region: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

class CustomerResponse(CustomerCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    documentation_url: Optional[str] = None

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TigerTeamMemberCreate(BaseModel):
    name: str
    email: str
    expertise_areas: Optional[List[str]] = None
    experience_years: Optional[int] = None

class TigerTeamMemberResponse(TigerTeamMemberCreate):
    id: int
    is_available: bool
    current_case_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SupportTicketCreate(BaseModel):
    ticket_number: str
    customer_id: int
    product_id: int
    title: str
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = "Open"

class SupportTicketResponse(SupportTicketCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    support_ticket_id: int
    customer_id: int
    product_id: int
    assigned_member_id: int
    title: str
    description: str
    desired_outcome: str
    priority: str = "Medium"

class CaseResponse(CaseCreate):
    id: int
    case_number: str
    status: str
    research_notes: Optional[str] = None
    ai_recommendations: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    first_customer_call_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class EvidenceCreate(BaseModel):
    case_id: int
    evidence_type: str
    content: str
    source: str
    relevance_score: Optional[int] = None

class EvidenceResponse(EvidenceCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
