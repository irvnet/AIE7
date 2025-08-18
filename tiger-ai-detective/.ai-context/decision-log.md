# Decision Log - IBM Tiger AI Detective

## 🎯 Project Foundation Decisions

### 2024-08-18: Project Scope and Timeline
**Decision**: One-week completion timeline for MVP
**Rationale**: User specified aggressive timeline to demonstrate rapid development capability
**Impact**: Influenced technology choices toward rapid prototyping over production-ready solutions

### 2024-08-18: Frontend Framework Selection
**Decision**: Streamlit over FastAPI frontend
**Rationale**: Based on `11_challenge` example for rapid MVP development
**Alternatives Considered**: FastAPI with separate frontend, React/Vue.js
**Impact**: Simplified development, faster time-to-market

### 2024-08-18: Package Management
**Decision**: uv over pip/poetry
**Rationale**: User preference for fast Python package management
**Impact**: Faster dependency resolution, better lock file management

## 🏗️ Architecture Decisions

### 2024-08-18: Database Strategy
**Decision**: SQLAlchemy ORM with SQLite for development, PostgreSQL for production
**Rationale**: 
- SQLAlchemy provides robust ORM capabilities
- SQLite for rapid development iteration
- PostgreSQL for Vercel deployment compatibility
**Impact**: Consistent data access patterns, easy deployment

### 2024-08-18: AI/ML Stack Selection
**Decision**: LangChain + LangGraph + OpenAI + Qdrant
**Rationale**:
- LangChain for LLM application framework
- LangGraph for stateful, multi-actor applications
- OpenAI for reliable, high-quality models
- Qdrant for vector database (in-memory for MVP)
**Impact**: Modern, well-supported AI stack with good documentation

### 2024-08-18: Vector Database Choice
**Decision**: Qdrant in-memory for MVP
**Rationale**: 
- Simple setup for rapid development
- No external dependencies for MVP
- Can be replaced with persistent storage later
**Impact**: Faster development, simpler deployment

## 📊 Data Model Decisions

### 2024-08-18: Core Entity Design
**Decision**: 6 core entities (Customer, Product, TigerTeamMember, SupportTicket, Case, Evidence)
**Rationale**: Covers complete support case lifecycle from initial ticket to resolution
**Impact**: Comprehensive data model for realistic scenarios

### 2024-08-18: Product Strategy Pivot
**Decision**: Change from generic IBM products to integration-focused stack
**Rationale**: 
- More strategic focus on IBM integration products
- Better alignment with real-world Tiger Team scenarios
- Easier to demonstrate cross-product complexity
**Products Selected**:
1. IBM WebSphere Application Server
2. Red Hat OpenShift
3. IBM Db2 Database
4. IBM MQ
5. IBM App Connect Enterprise
6. IBM API Connect

**Impact**: More realistic and valuable demo scenarios

## 🔧 Technical Implementation Decisions

### 2024-08-18: Mock Data Strategy
**Decision**: Integration-focused support scenarios instead of generic issues
**Rationale**: 
- More realistic Tiger Team scenarios
- Demonstrates cross-product complexity
- Better alignment with downloaded documentation
**Impact**: More compelling demo with real-world relevance

### 2024-08-18: Documentation Download Strategy
**Decision**: Focus on PDF sources (Redbooks/Redpapers) initially
**Rationale**:
- PDFs contain comprehensive technical content
- Easier to process for RAG system
- More structured than HTML documentation
**Impact**: 9 PDFs downloaded (85MB) providing rich technical content

### 2024-08-18: RAG Pattern Selection
**Decision**: Follow 11_challenge pattern for RAG implementation
**Rationale**:
- Proven pattern from existing codebase
- LangGraph state management for complex workflows
- Qdrant vector database integration
**Impact**: Consistent with existing codebase, proven approach

## 🐛 Problem Resolution Decisions

### 2024-08-18: SQLAlchemy Session Management
**Problem**: DetachedInstanceError when displaying cases
**Decision**: Implement proper session management with try/finally blocks
**Solution**: Explicit session management and querying within active sessions
**Impact**: Stable database operations, no more session errors

### 2024-08-18: Mock Data Content
**Problem**: Generic Faker text instead of integration-focused issues
**Decision**: Update SUPPORT_ISSUES list with realistic integration scenarios
**Solution**: 30+ specific integration issues spanning multiple IBM products
**Impact**: Realistic support scenarios for demo

### 2024-08-18: Date Parsing Issues
**Problem**: Can't parse date string '-6 months' in mock data
**Decision**: Use '-180d' format for better compatibility
**Solution**: Changed all date strings to use day-based format
**Impact**: Reliable mock data generation

### 2024-08-18: Database Integrity
**Problem**: UNIQUE constraint failed: products.name during generation
**Decision**: Clear database before regeneration
**Solution**: rm -f *.db before running mock data generation
**Impact**: Clean data generation without conflicts

## 📚 Documentation Decisions

### 2024-08-18: Sources Catalog Structure
**Decision**: JSON-based catalog with metadata for each source
**Rationale**:
- Structured approach to managing documentation sources
- Easy to extend and maintain
- Clear metadata for filtering and processing
**Impact**: Organized approach to documentation management

### 2024-08-18: Download Automation
**Decision**: Create automated download script with resume capability
**Rationale**:
- Consistent download process
- Resume capability for interrupted downloads
- Rate limiting to be respectful to servers
**Impact**: Reliable documentation acquisition

## 🚀 Deployment Decisions

### 2024-08-18: Target Platform
**Decision**: Vercel for deployment
**Rationale**: User preference, good Python support, easy deployment
**Impact**: Influenced database connection string handling

### 2024-08-18: Database Connection Handling
**Decision**: Replace postgres:// with postgresql:// for Vercel compatibility
**Rationale**: Vercel requires postgresql:// format for PostgreSQL connections
**Impact**: Ensures deployment compatibility

## 📋 Context Management Decisions

### 2024-08-18: Project Context Documentation
**Decision**: Create comprehensive PROJECT_CONTEXT.md
**Rationale**: 
- Maintain context across machines and sessions
- Document all key decisions and rationale
- Enable rapid context recovery
**Impact**: Better collaboration and context preservation

### 2024-08-18: AI Context Directory
**Decision**: Create .ai-context/ directory with structured files
**Rationale**:
- Organized approach to AI context management
- Separate concerns (coding standards, workflows, troubleshooting)
- Easy to maintain and update
**Impact**: Better AI assistant effectiveness across sessions

## 🔄 Future Decision Considerations

### RAG Implementation:
- **Pending**: PDF processing strategy (chunking, embedding)
- **Pending**: Vector database persistence strategy
- **Pending**: Integration with existing Streamlit app

### Performance Optimization:
- **Pending**: Database query optimization
- **Pending**: RAG retrieval optimization
- **Pending**: Caching strategy

### Deployment Strategy:
- **Pending**: Environment variable management
- **Pending**: Database migration strategy
- **Pending**: Monitoring and logging

---

**Last Updated**: August 18, 2024  
**Total Decisions**: 15 major decisions documented
