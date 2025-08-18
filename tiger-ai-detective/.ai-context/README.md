# AI Assistant Instructions - IBM Tiger AI Detective

## 🎯 Project Overview

**IBM Tiger Team Support System** - AI-powered support case management for IBM "Tiger Teams" (high-level product specialists) to shorten research time from 4 days to hours for difficult support cases.

### Core Mission:
- Connect customer evidence with product documentation and previous cases
- Provide recommendations for customer calls
- Web-based form for case submission
- Generate case records and team assignment
- **One-week completion timeline**

## 🏗️ Tech Stack

### Frontend:
- **Streamlit** - Based on `11_challenge` example for rapid MVP development

### Backend:
- **SQLAlchemy** - ORM for database interaction
- **Alembic** - Database migrations

### AI/ML:
- **LangChain** - LLM application framework
- **LangGraph** - Stateful, multi-actor applications
- **OpenAI GPT-4o-mini** - LLM for agents and RAG
- **OpenAI Embeddings (text-embedding-3-small)** - Vector embeddings
- **Qdrant** - Vector database (in-memory for MVP)

### Package Management:
- **uv** - Fast Python package manager

### Deployment:
- **Vercel** - Target deployment platform

## 📋 How to Work with This Project

### Always Check First:
1. **`PROJECT_CONTEXT.md`** - Current project status and decisions
2. **`git status`** - What's been changed
3. **`git log --oneline -3`** - Recent commits

### Development Commands:
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
```

### Key Patterns:
- **Follow 11_challenge RAG pattern** for AI implementation
- **Use integration-focused scenarios** (WebSphere + OpenShift + MQ + API Connect)
- **Commit frequently** with descriptive messages
- **Test changes** before committing
- **Update PROJECT_CONTEXT.md** for significant changes

### Environment Variables:
```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here  # Optional
DATABASE_URL=sqlite:///./tiger_team_support.db  # Development
```

## 🎯 Current Focus

### Integration-Focused Products:
1. IBM WebSphere Application Server
2. Red Hat OpenShift
3. IBM Db2 Database
4. IBM MQ
5. IBM App Connect Enterprise
6. IBM API Connect

### Next Steps:
1. Process downloaded PDFs for RAG
2. Implement vector database with Qdrant
3. Update main.py with RAG system
4. Test with integration scenarios

## 📁 Key Files

- **`app/main.py`** - Streamlit frontend
- **`app/models/`** - Database models and schemas
- **`data/documentation/`** - IBM PDFs (9 files, 85MB)
- **`scripts/`** - Automation scripts
- **`PROJECT_CONTEXT.md`** - Detailed project state

## 🚨 Common Issues

- **SQLAlchemy sessions**: Always use try/finally blocks
- **PDF downloads**: Check network connectivity
- **Mock data**: Clear database before regeneration
- **Dependencies**: Use `uv sync` not `pip install`

---

**Last Updated**: August 18, 2024  
**Status**: Ready for RAG implementation
