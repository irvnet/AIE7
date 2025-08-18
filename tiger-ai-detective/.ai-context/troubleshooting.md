# Troubleshooting Guide - IBM Tiger AI Detective

## 🚨 Common Issues and Solutions

### Database Issues

#### DetachedInstanceError: Parent instance is not bound to a Session
**Symptoms**: Error when trying to access related objects after session is closed
**Cause**: SQLAlchemy session management issues
**Solution**:
```python
# ❌ Wrong - session closed before accessing related objects
db = SessionLocal()
cases = db.query(Case).all()
db.close()
for case in cases:
    print(case.assigned_member.name)  # DetachedInstanceError

# ✅ Correct - query within active session
db = SessionLocal()
try:
    cases = db.query(Case).all()
    for case in cases:
        member = db.query(TigerTeamMember).filter(TigerTeamMember.id == case.assigned_member_id).first()
        print(member.name if member else "Unassigned")
finally:
    db.close()
```

#### UNIQUE constraint failed: products.name
**Symptoms**: Error during mock data generation
**Cause**: Database already contains products with same names
**Solution**:
```bash
# Clear database before regeneration
rm -f tiger_team_support.db
uv run python scripts/generate_mock_data.py
```

#### Database connection errors
**Symptoms**: Connection refused or timeout errors
**Cause**: Database URL issues or service not running
**Solution**:
```bash
# Check database connection
uv run python -c "from app.models.database import engine; print('DB OK')"

# For Vercel deployment, ensure postgresql:// format
DATABASE_URL="postgresql://user:pass@host:port/db"  # ✅ Correct
DATABASE_URL="postgres://user:pass@host:port/db"    # ❌ Wrong
```

### Package Management Issues

#### ModuleNotFoundError: No module named 'sqlalchemy'
**Symptoms**: Import errors for installed packages
**Cause**: Dependencies not installed or wrong environment
**Solution**:
```bash
# Install dependencies
uv sync

# Verify installation
uv run python -c "import sqlalchemy; print('SQLAlchemy OK')"
```

#### Virtual environment mismatch warnings
**Symptoms**: Warnings about VIRTUAL_ENV path mismatch
**Cause**: Multiple virtual environments or path issues
**Solution**:
```bash
# Use project-specific environment
uv sync --active

# Or ignore warnings (they don't affect functionality)
export UV_IGNORE_VIRTUAL_ENV=1
```

### Mock Data Generation Issues

#### Can't parse date string '-6 months'
**Symptoms**: Date parsing errors in mock data generation
**Cause**: Faker date format compatibility issues
**Solution**:
```python
# ❌ Wrong
fake.date_time_between(start_date='-6 months', end_date='now')

# ✅ Correct
fake.date_time_between(start_date='-180d', end_date='now')
```

#### Generic text instead of integration scenarios
**Symptoms**: Support tickets show generic Faker text
**Cause**: SUPPORT_ISSUES list not updated or used properly
**Solution**:
```python
# Ensure SUPPORT_ISSUES is used in generation
description = random.choice(SUPPORT_ISSUES)  # ✅ Use specific issues
# Not: description = fake.text(max_nb_chars=500)  # ❌ Generic text
```

### Documentation Download Issues

#### 403 Forbidden errors
**Symptoms**: PDF download fails with 403 error
**Cause**: URL requires authentication or has changed
**Solution**:
```bash
# Check URL manually
curl -I "https://www.ibm.com/docs/en/ibm-mq/9.2.x?topic=SSFKSJ_9.2.0/com.ibm.mq.pro.doc/q001040_.html"

# Skip problematic URLs or find alternative sources
# Update sources.catalog.json if needed
```

#### Network timeout errors
**Symptoms**: Download hangs or times out
**Cause**: Network connectivity or server issues
**Solution**:
```bash
# Check network connectivity
ping www.ibm.com

# Retry with longer timeout
# Modify download_documentation.py timeout parameter
response = requests.get(url, stream=True, timeout=60)  # Increase timeout
```

#### Partial downloads
**Symptoms**: PDF files are incomplete or corrupted
**Cause**: Network interruption during download
**Solution**:
```bash
# Clear partial downloads and retry
rm -f data/documentation/incomplete_file.pdf
uv run python scripts/download_documentation.py
```

### Streamlit App Issues

#### App not accessible
**Symptoms**: Streamlit app shows errors or won't start
**Cause**: Port conflicts or missing dependencies
**Solution**:
```bash
# Check if port is in use
lsof -i :8501

# Kill existing processes
pkill -f streamlit

# Start with specific port
uv run streamlit run app/main.py --server.port 8502
```

#### Import errors in Streamlit
**Symptoms**: ModuleNotFoundError when running app
**Cause**: Path issues or missing dependencies
**Solution**:
```python
# Add path to sys.path in main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### Session state issues
**Symptoms**: App state not persisting between interactions
**Cause**: Session state not properly initialized
**Solution**:
```python
# Initialize session state
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
```

### RAG System Issues

#### OpenAI API errors
**Symptoms**: API key errors or rate limiting
**Cause**: Invalid API key or quota exceeded
**Solution**:
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
uv run python -c "from openai import OpenAI; client = OpenAI(); print('API OK')"
```

#### Vector database errors
**Symptoms**: Qdrant connection or embedding errors
**Cause**: Memory issues or embedding model problems
**Solution**:
```python
# Use in-memory Qdrant for development
qdrant_vectorstore = Qdrant.from_documents(
    documents=chunks,
    embedding=embedding_model,
    location=":memory:"  # In-memory for development
)
```

#### PDF processing errors
**Symptoms**: PyMuPDFLoader fails to load PDFs
**Cause**: Corrupted PDFs or missing dependencies
**Solution**:
```bash
# Install PyMuPDF
uv add pymupdf

# Check PDF integrity
uv run python -c "import fitz; doc = fitz.open('data/documentation/test.pdf'); print('PDF OK')"
```

## 🔍 Debugging Steps

### System Health Check
```bash
# Run comprehensive health check
uv run python test_system.py

# Check individual components
uv run python -c "from app.models.database import engine; print('Database: OK')"
uv run python -c "import streamlit; print('Streamlit: OK')"
uv run python -c "from langchain_openai import OpenAIEmbeddings; print('LangChain: OK')"
```

### Database Debugging
```bash
# Check database schema
uv run python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine); print('Schema: OK')"

# Check data
uv run python -c "from app.models.database import SessionLocal; from app.models.schemas import Product; db = SessionLocal(); print(f'Products: {db.query(Product).count()}'); db.close()"
```

### Network Debugging
```bash
# Check connectivity
ping www.ibm.com
curl -I https://www.ibm.com

# Check DNS
nslookup www.ibm.com
```

### Memory and Performance
```bash
# Check memory usage
ps aux | grep python

# Check disk space
df -h

# Check large files
du -h data/documentation/*.pdf | sort -hr
```

## 🛠️ Recovery Procedures

### Complete System Reset
```bash
# 1. Clear all generated files
rm -f *.db
rm -rf data/documentation/*.pdf

# 2. Reinstall dependencies
uv sync

# 3. Regenerate everything
uv run python setup.py
uv run python scripts/download_documentation.py
uv run python scripts/generate_mock_data.py

# 4. Test system
uv run python test_system.py
```

### Database Recovery
```bash
# 1. Backup current database (if needed)
cp tiger_team_support.db tiger_team_support.db.backup

# 2. Clear and regenerate
rm -f tiger_team_support.db
uv run python scripts/generate_mock_data.py

# 3. Verify data
uv run python -c "from app.models.database import SessionLocal; from app.models.schemas import Customer; db = SessionLocal(); print(f'Customers: {db.query(Customer).count()}'); db.close()"
```

### Documentation Recovery
```bash
# 1. Clear downloads
rm -rf data/documentation/*.pdf

# 2. Redownload
uv run python scripts/download_documentation.py

# 3. Verify downloads
ls -la data/documentation/
du -h data/documentation/
```

## 📞 Getting Help

### Check These First:
1. **PROJECT_CONTEXT.md** - Current project status
2. **.ai-context/README.md** - AI instructions
3. **Recent commits** - What changed recently
4. **Environment variables** - API keys and configuration

### Common Solutions:
- **Restart the system** - Often fixes transient issues
- **Clear and regenerate** - For data-related issues
- **Check dependencies** - Run `uv sync`
- **Verify API keys** - Check environment variables

### When to Ask for Help:
- **Persistent errors** after trying solutions above
- **New error patterns** not documented here
- **Performance issues** affecting usability
- **Deployment problems** not covered in troubleshooting

---

**Last Updated**: August 18, 2024  
**Common Issues**: 15 documented solutions
