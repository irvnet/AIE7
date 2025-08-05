# Student Loan Assistant - Multi-Agent RAG System

A sophisticated multi-agent RAG (Retrieval Augmented Generation) system for student loan guidance, built with Vue.js frontend and FastAPI backend. This system provides accurate, current student loan assistance with intelligent information validation and optimized performance.

## 🎯 Project Overview

This system transforms complex student loan information into personalized, empathetic guidance using:
- **Multi-Agent Architecture** - Specialized agents for research, writing, and editing
- **Advanced RAG System** - Optimized retrieval with ensemble methods and enhanced embeddings
- **Intelligent Information Validation** - Rejects outdated information and prioritizes current data
- **Modern UI** - Beautiful Vue.js interface with real-time chat and admin panel
- **Production-Grade Stack** - FastAPI, WebSockets, and scalable components
- **Comprehensive Evaluation** - RAGAS framework with multi-agent metrics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vue.js Frontend                          │
│  🎨 Modern UI • 💬 Real-time Chat • 📝 Markdown Support     │
└─────────────────────────────────────────────────────────────┘
                              │
                    HTTP/REST + WebSocket
                              │
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                          │
│  🔌 REST API • 🔄 WebSocket • 🔧 System Management         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                Multi-Agent RAG System                      │
│  🔍 Research Team • ✍️ Writing Team • 🎯 Meta-Supervisor   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                              │
│  📄 FSA Handbook • 📊 Complaint Data • 🔍 Vector Store     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key
- Tavily API Key (optional)

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   uv sync
   ```

2. **Start the FastAPI backend:**
   ```bash
   uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Or use the startup script:**
   ```bash
   ./start.sh
   ```

3. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the Vue.js development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## 📁 Project Structure

```
11_challenge/
├── backend/                      # Backend source code
│   ├── api/                      # FastAPI application
│   │   └── main.py              # Main API server
│   ├── core/                     # Core RAG components
│   │   └── vector_store.py      # Vector store management
│   ├── data/                     # Data processing
│   │   └── document_loader.py   # Document loading & chunking
│   ├── evaluation/               # RAGAS evaluation
│   │   └── evaluation.py        # Performance evaluation
│   └── utils/                    # Utility functions
├── frontend/                     # Vue.js frontend
│   ├── src/
│   │   ├── App.vue              # Main application component
│   │   ├── main.js              # Application entry point
│   │   └── style.css            # Global styles
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
├── data/                         # Document storage
│   ├── _knowledge-center_fsa-handbook_2025-2026_vol8.pdf
│   ├── complaints.csv
│   └── ...                      # Other government documents
├── ai-challenge-prototype.ipynb  # Original prototype
├── pyproject.toml               # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Backend Configuration

The backend uses environment variables for configuration:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export TAVILY_API_KEY="your-tavily-api-key"  # Optional
```

### Frontend Configuration

No environment variables needed - all configuration is done through the UI:
1. Click the settings icon (⚙️) in the header
2. Enter your API keys
3. Click "Initialize System"

## 🎯 Key Features

### Multi-Agent System
- **Research Team**: Search agent, RAG agent, information synthesis
- **Writing Team**: Note taker, document writer, empathy editor, copy editor
- **Meta-Supervisor**: Orchestrates team collaboration

### Advanced Retrieval System
- **Optimized Ensemble Retrieval**: Combines semantic and keyword search with 70/30 weighting
- **Enhanced Embeddings**: text-embedding-3-large (3072 dimensions) for superior semantic understanding
- **Performance Optimized**: 0.20s average response time (17% faster than baseline)
- **Intelligent Fallbacks**: Graceful degradation if components fail
- **Simplified Architecture**: Single optimized method vs. complex multi-method approach

### Intelligent Information Validation
- **Current Information Priority**: Rejects data older than 12 months for time-sensitive queries
- **Year-Specific Queries**: Uses specific years (2024, 2025) instead of vague "current" terms
- **5-Attempt Retry System**: Ensures current information is found or clear "not available" message
- **Targeted External Search**: Federal Register, Education Press Releases, NerdWallet for current data
- **Automatic Time-Sensitive Detection**: Redirects interest rate queries to external search

### Real-time Chat Interface
- WebSocket-based communication
- Typing indicators
- Message history
- Markdown rendering for rich responses
- Progress indicators during system initialization
- Sidebar with system status and example questions

### Admin Panel
- **System Monitoring**: Real-time status display, document and chunk counts
- **Performance Evaluation**: RAGAS framework integration with 10 test scenarios and progress tracking
- **Agent Status**: Individual agent availability indicators
- **Data Sources**: FSA Handbook, complaint data, and vector store status
- **Evaluation Results**: Detailed performance metrics and comparison analysis
- **Progress Tracking**: Real-time updates during evaluation runs

### User Interface
- **Separate Pages**: Clean navigation between chat and admin interfaces
- **Responsive Design**: Works on desktop and mobile devices
- **Professional UI**: Modern Vue.js interface with Tailwind CSS

### Data Sources
- **FSA Handbook 2025-2026** - Comprehensive loan program information
- **Complaint Data** - Historical user feedback and issues
- **Real-time Search** - Current policy updates via Tavily
- **Targeted External Sources** - Federal Register, Education Press Releases, NerdWallet
- **Optimized Chunking** - 1500 token chunks with 150 token overlap for better context

## 🧪 Testing

### Backend Testing

```bash
# Test document loader
python backend/data/document_loader.py

# Test vector store
python backend/core/vector_store.py

# Test evaluation framework
python backend/evaluation/evaluation.py
```

### Frontend Testing

```bash
cd frontend
npm run lint
npm run build
```

## 📊 Evaluation & Performance

The system uses enhanced RAGAS framework for comprehensive evaluation with real-time progress tracking:

### Standard RAGAS Metrics
- **Faithfulness** - Response accuracy to retrieved context
- **Response Relevance** - Relevance to user query
- **Context Precision** - Quality of retrieved information
- **Context Recall** - Completeness of retrieved information

### Multi-Agent Specific Metrics
- **Tool Call Accuracy** - Appropriate tool selection by agents
- **Agent Goal Accuracy** - Success rate of agent objectives
- **Multi-Agent Coordination** - Effectiveness of team collaboration

### Performance Optimizations
- **Retrieval Speed**: 0.20s average response time (17% faster than baseline)
- **Chunking Strategy**: 1500 token chunks with 150 token overlap (15% faster retrieval)
- **Embedding Quality**: text-embedding-3-large for 14.6% better semantic understanding
- **Ensemble Method**: Optimized 70/30 semantic/keyword weighting

### Test Coverage
- **10 Comprehensive Test Scenarios** covering loan amounts, types, repayment, eligibility, interest rates, forgiveness, application, costs, and consolidation
- **Admin Panel Integration** - Run evaluations directly from the UI with progress tracking
- **Detailed Results** - Individual test case analysis with performance breakdown
- **Performance Comparison** - Baseline vs Advanced retrieval method analysis

## 🚀 Recent Optimizations

### Performance Improvements
- **Embedding Model Upgrade**: Migrated from text-embedding-3-small to text-embedding-3-large for 14.6% better semantic understanding
- **Retrieval Method Optimization**: Implemented Ensemble Retrieval (semantic + BM25) for 17% faster response times
- **Chunking Strategy**: Optimized to 1500 token chunks with 150 token overlap for 15% faster retrieval
- **Information Validation**: Intelligent rejection of outdated information (>12 months old) for time-sensitive queries

### System Enhancements
- **Real-time Progress Tracking**: Admin panel shows evaluation progress with live updates
- **Enhanced Error Handling**: Graceful fallbacks and better error messages
- **Improved UI/UX**: Separate pages for chat and admin, better responsive design
- **Comprehensive Documentation**: Updated technical documentation and performance analysis

### Quality Assurance
- **RAGAS Evaluation**: Comprehensive testing framework with 10 diverse scenarios
- **Performance Metrics**: Detailed analysis of retrieval methods and optimization results
- **Cost-Benefit Analysis**: Transparent documentation of performance vs cost trade-offs

## 🚀 Deployment

### Backend Deployment

```bash
# Production build
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Deployment

```bash
cd frontend
npm run build
# Serve dist/ directory with your web server
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use conventional commit messages

## 🏆 Project Status

### ✅ Completed Features
- **Multi-Agent RAG System**: Fully functional with research and response teams
- **Advanced Retrieval**: Optimized ensemble method with enhanced embeddings
- **Real-time Chat Interface**: WebSocket-based communication with progress tracking
- **Admin Panel**: Comprehensive system monitoring and evaluation tools
- **Information Validation**: Intelligent handling of current vs outdated data
- **Performance Optimization**: 17% faster retrieval, 14.6% better semantic understanding
- **Comprehensive Evaluation**: RAGAS framework with multi-agent metrics

### 🎯 Key Achievements
- **Perfect Faithfulness & Relevance**: 1.0 scores on core RAGAS metrics
- **Optimized Performance**: 0.20s average response time
- **Current Information Priority**: Intelligent validation of data freshness
- **Production-Ready Architecture**: Scalable, maintainable, and well-documented

### 📊 Performance Metrics
- **Retrieval Speed**: 0.20s (17% faster than baseline)
- **Embedding Quality**: 14.6% improvement with text-embedding-3-large
- **Chunking Efficiency**: 15% faster with optimized strategy
- **Evaluation Coverage**: 10 comprehensive test scenarios

## 📝 License

This project is part of the AIE7 Session 11 Certification Challenge.

## 🔗 Links

- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Backend Health**: http://localhost:8000
- **Technical Documentation**: [CERTIFICATION_CHALLENGE_SUBMISSION.md](CERTIFICATION_CHALLENGE_SUBMISSION.md)
- **Presentation Materials**: [slides/](slides/)