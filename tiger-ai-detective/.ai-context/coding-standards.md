# Coding Standards - IBM Tiger AI Detective

## 🐍 Python Standards

### Code Style:
- **PEP 8** compliance
- **Type hints** for all function parameters and return values
- **Docstrings** for all functions and classes
- **F-strings** for string formatting (Python 3.6+)
- **Line length**: 88 characters (Black formatter)

### Naming Conventions:
- **snake_case** for variables, functions, and modules
- **PascalCase** for classes
- **UPPER_CASE** for constants
- **Descriptive names** - avoid abbreviations

### Imports:
```python
# Standard library imports first
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import streamlit as st
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI

# Local imports
from app.models.database import SessionLocal
from app.models.schemas import Customer, Product
```

### Error Handling:
```python
try:
    # Database operations
    db = SessionLocal()
    try:
        result = db.query(Model).all()
        return result
    finally:
        db.close()
except Exception as e:
    logger.error(f"Database error: {e}")
    raise
```

## 🗄️ Database Standards

### SQLAlchemy Patterns:
- **Use ORM models** defined in `app/models/schemas.py`
- **Session management** with try/finally blocks
- **Connection pooling** for production
- **Migration scripts** with Alembic

### Model Definitions:
```python
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    support_tickets = relationship("SupportTicket", back_populates="customer")
```

### Pydantic Schemas:
```python
class CustomerCreate(BaseModel):
    name: str
    company: str
    
class CustomerResponse(BaseModel):
    id: int
    name: str
    company: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 🧪 Testing Standards

### Test Structure:
- **pytest** framework
- **Test files** in `tests/` directory
- **Test functions** prefixed with `test_`
- **Descriptive test names**

### Test Examples:
```python
def test_customer_creation():
    """Test customer creation with valid data"""
    customer_data = {
        "name": "John Doe",
        "company": "Test Corp"
    }
    customer = Customer(**customer_data)
    assert customer.name == "John Doe"
    assert customer.company == "Test Corp"

def test_database_connection():
    """Test database connection and basic operations"""
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()
```

### Mock Data:
- **Use Faker** for realistic test data
- **Integration scenarios** for IBM products
- **Cross-platform issues** for realistic testing

## 🔧 Project-Specific Standards

### Streamlit Patterns:
```python
# Page configuration
st.set_page_config(
    page_title="IBM Tiger AI Detective",
    page_icon="🦁",
    layout="wide"
)

# Session state management
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False

# Error handling
try:
    # Streamlit operations
    st.success("Operation completed!")
except Exception as e:
    st.error(f"Error: {e}")
```

### LangChain Patterns:
```python
# RAG system setup
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
qdrant_vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embedding_model,
    location=":memory:"
)

# LangGraph state management
class State(TypedDict):
    question: str
    context: List
    response: str
```

### File Organization:
```
app/
├── __init__.py
├── main.py              # Streamlit frontend
└── models/
    ├── __init__.py
    ├── database.py      # SQLAlchemy setup
    └── schemas.py       # ORM models and Pydantic schemas

scripts/
├── download_documentation.py  # PDF download automation
└── generate_mock_data.py      # Mock data generation

tests/
└── test_basic.py       # Basic unit tests
```

## 📝 Documentation Standards

### Code Comments:
- **Explain WHY**, not WHAT
- **Complex business logic** requires comments
- **Integration scenarios** need context

### README Files:
- **Clear setup instructions**
- **Environment variables**
- **Development commands**
- **Troubleshooting section**

### Commit Messages:
- **Conventional commits** format
- **Descriptive messages**
- **Reference issues** if applicable

Example:
```
feat: Add IBM documentation download system and integration-focused mock data

- Add sources.catalog.json with 20 IBM documentation sources
- Create download_documentation.py script for automated PDF downloads
- Successfully download 9 IBM documentation PDFs (85MB total)
- Update mock data with integration-focused product mix
```

## 🚨 Common Anti-Patterns to Avoid

### Database:
- ❌ **DetachedInstanceError**: Always manage sessions properly
- ❌ **Hardcoded SQL**: Use ORM models
- ❌ **No error handling**: Always use try/finally

### Python:
- ❌ **String concatenation**: Use f-strings
- ❌ **No type hints**: Always add types
- ❌ **Generic exceptions**: Catch specific exceptions

### Testing:
- ❌ **No tests**: Write tests for new features
- ❌ **Hardcoded test data**: Use Faker
- ❌ **No cleanup**: Clean up test data

---

**Last Updated**: August 18, 2024
