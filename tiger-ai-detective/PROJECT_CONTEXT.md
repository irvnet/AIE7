# IBM Tiger AI Detective - Project Context

## 🎯 Project Overview

**IBM Tiger Team Support System** - An AI-powered support case management system for IBM "Tiger Teams" (high-level product specialists) to shorten research time from 4 days to hours for difficult support cases.

### Core Mission:
- Connect customer evidence with product documentation and previous cases
- Provide recommendations for customer calls
- Web-based form for case submission
- Generate case records and team assignment
- **One-week completion timeline**

## 🏗️ Architecture Decisions

### Frontend Framework:
- **Streamlit** (chosen over FastAPI frontend)
- **Rationale**: Based on `11_challenge` example for rapid MVP development
- **Pattern**: Follow `11_challenge/temp/app.py` structure

### Backend Framework:
- **FastAPI** initially considered, but **Streamlit** became primary app
- **SQLAlchemy** for ORM and database interaction
- **Alembic** for database migrations

### AI/ML Stack:
- **LangChain** for building LLM applications
- **LangGraph** for stateful, multi-actor applications
- **OpenAI GPT-4o-mini** for LLM agents and RAG
- **OpenAI Embeddings (text-embedding-3-small)** for vector embeddings
- **Qdrant** vector database (in-memory for MVP)
- **uv** for fast Python package management
- **Vercel** for target deployment platform

## 📊 Data Model Decisions

### Core Entities:
1. **Customer** - Company information and contact details
2. **Product** - IBM products with versions and documentation URLs
3. **TigerTeamMember** - Specialist information and availability
4. **SupportTicket** - Original support tickets from customers
5. **Case** - Tiger Team cases with research notes and AI recommendations
6. **Evidence** - Supporting evidence and documentation

### Database Strategy:
- **SQLite** for development
- **PostgreSQL** for Vercel deployment
- **Connection handling**: Replace `postgres://` with `postgresql://` for Vercel compatibility

## 🎯 Product Strategy Decisions

### Integration-Focused Product Mix:
**Changed from generic IBM products to strategic integration stack:**

1. **IBM WebSphere Application Server** - Application Server
2. **Red Hat OpenShift** - Container Platform
3. **IBM Db2 Database** - Database
4. **IBM MQ** - Messaging
5. **IBM App Connect Enterprise** - Integration
6. **IBM API Connect** - API Management

### Strategic Benefits:
- **Integration Stack**: Covers full integration lifecycle
- **Hybrid Cloud**: OpenShift + WebSphere for deployment flexibility
- **API Management**: API Connect for external integrations
- **Messaging**: MQ for reliable message delivery
- **Data**: Db2 for enterprise data management
- **Integration Platform**: App Connect for connecting everything

## 🔧 Technical Implementation Decisions

### Mock Data Strategy:
- **Faker** for realistic data generation
- **Integration-focused support issues** instead of generic problems
- **Cross-platform scenarios** that span multiple IBM products

### Support Issues (Updated):
**Realistic integration scenarios that require Tiger Team expertise:**

- API Gateway authentication failures between WebSphere and API Connect
- Message queue connection timeouts in OpenShift containerized MQ deployments
- Database connection pool exhaustion in containerized Db2 on OpenShift
- SSL/TLS certificate validation failures in OpenShift to WebSphere communication
- WebSphere cluster node communication failures in hybrid cloud environment
- App Connect integration flow deployment failures in OpenShift
- API Connect rate limiting and throttling issues affecting WebSphere applications
- MQ message delivery failures in hybrid cloud environments
- OpenShift pod scaling and resource allocation problems with Db2
- Cross-platform integration authentication issues between MQ and App Connect
- Container registry connectivity problems affecting OpenShift deployments
- Service mesh routing failures in microservices between WebSphere and API Connect
- Database performance degradation in containerized Db2 on OpenShift
- API versioning and backward compatibility issues in API Connect
- Integration flow monitoring and alerting failures in App Connect
- Cross-platform data transformation errors between Db2 and MQ
- Load balancer configuration issues in OpenShift affecting WebSphere
- Message persistence and recovery problems in MQ cluster
- API security token validation failures in API Connect
- Container resource limits causing application failures in OpenShift
- WebSphere to OpenShift migration authentication issues
- MQ message ordering and delivery guarantees in distributed environment
- App Connect integration flow performance degradation under load
- API Connect API gateway routing failures in multi-region deployment
- Db2 database connection failures in containerized environment
- Cross-product SSL certificate chain validation issues
- Integration flow deadlock scenarios in App Connect
- API Connect rate limiting bypass attempts and security incidents
- OpenShift pod eviction causing MQ message loss
- WebSphere cluster split-brain scenarios in hybrid cloud

## 📚 Documentation Strategy

### Sources Catalog:
**Created `data/sources.catalog.json` with 20 IBM documentation sources:**

- **IBM MQ**: 5 sources (Product docs, Redbooks, Redpapers, Support KB)
- **WebSphere Application Server**: 3 sources (Product docs, Redbooks)
- **IBM Db2**: 3 sources (Product docs, Redbooks)
- **IBM App Connect Enterprise**: 3 sources (Product docs, Redbooks)
- **IBM API Connect**: 4 sources (Product docs, Redpapers)
- **Red Hat OpenShift**: 2 sources (Product docs, IBM Cloud integration)

### Download Strategy:
- **Focus on PDF sources** (Redbooks/Redpapers) for comprehensive content
- **Skip HTML-only sources** initially
- **Resume capability** for interrupted downloads
- **Rate limiting** (1-second delay) to be respectful to servers

### Downloaded Documentation (9 PDFs, 85MB total):
1. **`sg248351.pdf` (11MB)** - "A Practical Guide for IBM Hybrid Integration Platform" ⭐
2. **`sg248536.pdf` (17MB)** - "Db2 13 for z/OS Performance Topics"
3. **`sg247971.pdf` (12MB)** - "WebSphere Application Server V8: Administration and Configuration"
4. **`sg248056.pdf` (11MB)** - "WebSphere Application Server V8.5 Administration and Configuration Guide"
5. **`redp5350.pdf` (6.1MB)** - "Getting Started with IBM API Connect: Scenarios Guide" ⭐
6. **`sg248383.pdf` (5.8MB)** - "DB2 12 for z/OS Technical Overview"
7. **`sg248218.pdf` (4.7MB)** - "IBM MQ V8 Features and Enhancements"
8. **`redp5349.pdf` (3.4MB)** - "Getting Started with IBM API Connect: Concepts & Architecture" ⭐
9. **`redp0021.pdf` (1.4MB)** - "WebSphere MQ Primer: An Introduction to Messaging" ⭐

## 🔄 RAG System Design (Based on 11_challenge)

### Pattern from 11_challenge:
```python
# Document Loading & Processing
directory_loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyMuPDFLoader)
documents = directory_loader.load()

# Chunk documents with token-aware splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=750,
    chunk_overlap=0,
    length_function=tiktoken_len,
)
chunks = text_splitter.split_documents(documents)

# Vector Database Creation
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
qdrant_vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embedding_model,
    location=":memory:"
)
retriever = qdrant_vectorstore.as_retriever()

# LangGraph State Management
class State(TypedDict):
    question: str
    context: List
    response: str

def retrieve(state: State) -> State:
    retrieved_docs = retriever.invoke(state["question"])
    return {"context": retrieved_docs}

def generate(state: State) -> State:
    generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
    response = generator_chain.invoke({"query": state["question"], "context": state["context"]})
    return {"response": response}

# Build graph
graph_builder = StateGraph(State)
graph_builder = graph_builder.add_sequence([retrieve, generate])
rag_graph = graph_builder.compile()
```

### Tiger Team Adaptations:
- **Multiple knowledge sources**: IBM docs + support cases + product knowledge
- **Cross-product relationships**: WebSphere + MQ + API Connect scenarios
- **Integration scenarios**: Real-world deployment issues
- **Tiger Team expertise**: Specialized troubleshooting knowledge

## 🐛 Issues Resolved

### SQLAlchemy Session Management:
- **Problem**: `DetachedInstanceError` when displaying cases
- **Solution**: Proper session management with `try...finally` blocks
- **Fix**: Explicit querying of related objects within active session

### Mock Data Generation:
- **Problem**: Generic Faker text instead of integration-focused issues
- **Solution**: Updated `SUPPORT_ISSUES` list with realistic integration scenarios
- **Fix**: Modified ticket and case generation to use specific issues

### Date Parsing:
- **Problem**: `Can't parse date string '-6 months'` in mock data
- **Solution**: Changed to `'-180d'` format for better compatibility

### Database Integrity:
- **Problem**: `UNIQUE constraint failed: products.name` during generation
- **Solution**: Clear database before regeneration with `rm -f *.db`

## 📁 Project Structure

```
tiger-ai-detective/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Streamlit frontend
│   └── models/
│       ├── __init__.py
│       ├── database.py         # SQLAlchemy setup
│       └── schemas.py          # ORM models and Pydantic schemas
├── data/
│   ├── sources.catalog.json    # IBM documentation sources
│   └── documentation/          # Downloaded PDFs (9 files, 85MB)
├── scripts/
│   ├── download_documentation.py  # PDF download automation
│   └── generate_mock_data.py      # Mock data generation
├── tests/
│   └── test_basic.py          # Basic unit tests
├── .ai-context/               # AI-specific context files
├── pyproject.toml             # Project configuration (uv)
├── requirements.txt           # Dependencies
├── run_app.py                # Application launcher
├── setup.py                  # Project setup automation
├── Makefile                  # Development commands
├── vercel.json               # Vercel deployment config
└── README.md                 # Project documentation
```

## 🚀 Current Status

### ✅ Completed:
- [x] Project structure and configuration
- [x] Database models and schemas
- [x] Integration-focused product mix
- [x] Realistic support scenarios
- [x] Mock data generation system
- [x] Documentation sources catalog
- [x] PDF download automation
- [x] 9 IBM documentation PDFs downloaded (85MB)
- [x] Basic Streamlit frontend
- [x] Database session management fixes
- [x] Git repository with clean commit history
- [x] AI context directory with comprehensive documentation

### 🔄 In Progress:
- [ ] RAG system implementation
- [ ] PDF processing and chunking
- [ ] Vector database creation
- [ ] Integration with existing app

### 📋 Next Steps:
1. **Process PDFs** for text extraction and chunking
2. **Create vector embeddings** using OpenAI
3. **Build Qdrant vector database** 
4. **Update main.py** with RAG system using 11_challenge pattern
5. **Test with integration scenarios**
6. **Deploy to Vercel**

## 🎯 Key Success Metrics

### Demo Value:
- **Cross-product complexity** that requires Tiger Team expertise
- **Integration challenges** that span multiple IBM products
- **Real-world scenarios** that would actually require days of research
- **AI value** in connecting evidence across products and previous cases

### Technical Goals:
- **Testable, maintainable code**
- **Clean commits** at key stopping points
- **Realistic mock data** for customers, users, IBM products, and support tickets
- **One-week completion timeline**

## 🔑 Environment Variables Needed

```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here  # Optional for web search
DATABASE_URL=sqlite:///./tiger_team_support.db  # For development
```

## 📝 Development Commands

```bash
# Setup
uv sync                    # Install dependencies
uv run python setup.py     # Setup project

# Development
uv run streamlit run app/main.py  # Run app
uv run python scripts/generate_mock_data.py  # Generate mock data
uv run python scripts/download_documentation.py  # Download docs

# Testing
uv run python -m pytest tests/  # Run tests
uv run python test_system.py    # System health check

# Code Quality
make format                  # Format code
make lint                    # Lint code
make typecheck               # Type checking
```

---

**Last Updated**: August 18, 2024  
**Current Commit**: `9ec8e22` - "feat: Add IBM documentation download system and integration-focused mock data"  
**Status**: Ready for RAG implementation
