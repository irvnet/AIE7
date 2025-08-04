# Student Loan Assistant - Multi-Agent RAG System

A sophisticated multi-agent RAG (Retrieval Augmented Generation) system for student loan guidance, built with Vue.js frontend and FastAPI backend.

## 🎯 Project Overview

This system transforms complex student loan information into personalized, empathetic guidance using:
- **Multi-Agent Architecture** - Specialized agents for research, writing, and editing
- **RAG System** - Retrieval from government documents and real-time search
- **Modern UI** - Beautiful Vue.js interface with real-time chat
- **Production-Grade Stack** - FastAPI, WebSockets, and scalable components

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
- **BM25 Retrieval**: Traditional keyword-based retrieval for exact term matching
- **Multi-Query Retrieval**: LLM-generated query variations for improved recall
- **Parent Document Retrieval**: Small-to-big strategy for better context preservation
- **Contextual Compression**: Reranking using Cohere's rerank-v3.5 model
- **Ensemble Retrieval**: Reciprocal Rank Fusion combining all techniques
- **Graceful Degradation**: System works even if some techniques fail

### Real-time Chat Interface
- WebSocket-based communication
- Typing indicators
- Message history
- Markdown rendering for rich responses
- Progress indicators during system initialization
- Sidebar with system status and example questions

### Admin Panel
- **System Monitoring**: Real-time status display, document and chunk counts
- **Performance Evaluation**: RAGAS framework integration with 10 test scenarios
- **Agent Status**: Individual agent availability indicators
- **Data Sources**: FSA Handbook, complaint data, and vector store status

### User Interface
- **Separate Pages**: Clean navigation between chat and admin interfaces
- **Responsive Design**: Works on desktop and mobile devices
- **Professional UI**: Modern Vue.js interface with Tailwind CSS

### Data Sources
- **FSA Handbook 2025-2026** - Comprehensive loan program information
- **Complaint Data** - Historical user feedback and issues
- **Real-time Search** - Current policy updates via Tavily

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

## 📊 Evaluation

The system uses enhanced RAGAS framework for comprehensive evaluation:

### Standard RAGAS Metrics
- **Faithfulness** - Response accuracy to retrieved context
- **Response Relevance** - Relevance to user query
- **Context Precision** - Quality of retrieved information
- **Context Recall** - Completeness of retrieved information

### Multi-Agent Specific Metrics
- **Tool Call Accuracy** - Appropriate tool selection by agents
- **Agent Goal Accuracy** - Success rate of agent objectives
- **Multi-Agent Coordination** - Effectiveness of team collaboration

### Test Coverage
- **10 Comprehensive Test Scenarios** covering loan amounts, types, repayment, eligibility, interest rates, forgiveness, application, costs, and consolidation
- **Admin Panel Integration** - Run evaluations directly from the UI
- **Detailed Results** - Individual test case analysis with performance breakdown

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

## 📝 License

This project is part of the AIE7 Session 11 Certification Challenge.

## 🔗 Links

- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Backend Health**: http://localhost:8000