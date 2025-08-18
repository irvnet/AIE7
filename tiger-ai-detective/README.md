# 🦁 IBM Tiger Team Support Case Management System

An AI-powered support case management system designed specifically for IBM Tiger Teams - high-level product specialists who handle the most critical support issues worldwide.

## 🎯 Overview

This system helps Tiger Team members:
- **Reduce research time** from 4 days to hours through AI assistance
- **Connect evidence** with product documentation and previous cases
- **Generate recommendations** for customer calls
- **Manage multiple cases** simultaneously (up to 5 cases per specialist)

## 🚀 Features

### Core Functionality
- **Case Management**: Create and track Tiger Team cases
- **AI Research Assistant**: RAG-powered research on IBM products and issues
- **Customer History**: Track customer support history and patterns
- **Product Knowledge**: IBM product documentation and troubleshooting guides
- **Team Assignment**: Intelligent assignment to available specialists
- **Evidence Collection**: Store and analyze case evidence

### AI Capabilities
- **RAG System**: Retrieval Augmented Generation for IBM documentation
- **Case Analysis**: AI-powered case research and recommendations
- **Pattern Recognition**: Identify similar cases across customers
- **Solution Suggestions**: Generate potential solutions based on historical data

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI API   │    │   AI Agents     │
│   (Case Mgmt)   │◄──►│   (REST/GraphQL)│◄──►│   (RAG Pipeline)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQL + Vector)│
                       └─────────────────┘
```

## 📋 Data Models

### Core Entities
- **Customer**: Company information and support history
- **Product**: IBM products (WebSphere, Db2, MQ, etc.)
- **SupportTicket**: Original support tickets from customers
- **Case**: Tiger Team cases with research and recommendations
- **TigerTeamMember**: Specialist information and availability
- **Evidence**: Case evidence and analysis

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based web interface)
- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Vector DB**: Qdrant (for RAG system)
- **AI**: OpenAI GPT-4 + LangChain + LangGraph
- **Package Manager**: uv (fast Python package manager)
- **Deployment**: Vercel-ready

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- uv (Python package manager)
- OpenAI API key
- Git

### Installation

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ibm-tiger-team-support
   ```

3. **Run the setup script**
   ```bash
   python setup.py
   ```

4. **Run the application**
   ```bash
   uv run python run_app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

### Manual Setup (Alternative)

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Generate mock data**
   ```bash
   uv run python scripts/generate_mock_data.py
   ```

3. **Run the application**
   ```bash
   uv run streamlit run app/main.py
   ```

### Configuration

1. **Set up API keys**
   - Add your OpenAI API key in the Streamlit sidebar
   - Click "Initialize System" to start the AI components

2. **Create your first case**
   - Fill out the case creation form
   - Assign to an available Tiger Team member
   - Review AI-generated research recommendations

## 📊 Mock Data

The system includes realistic mock data for:
- **50+ Customers** across various industries
- **8 IBM Products** (WebSphere, Db2, MQ, Cloud Pak, etc.)
- **15 Tiger Team Members** with different expertise areas
- **200+ Support Tickets** with various issues
- **30+ Active Cases** with research notes and recommendations

## 🔧 Development

### Project Structure
```
├── app/
│   ├── main.py              # Streamlit application
│   ├── models/              # Database models and schemas
│   ├── api/                 # FastAPI endpoints
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── scripts/
│   └── generate_mock_data.py # Mock data generator
├── tests/                   # Test files
├── data/                    # Data files
├── pyproject.toml          # Project configuration (uv)
└── requirements.txt        # Dependencies (legacy)
```

### Development Commands
```bash
# Run tests
uv run pytest

# Format code
uv run black app/

# Sort imports
uv run isort app/

# Lint code
uv run flake8 app/

# Type checking
uv run mypy app/

# Run the application
uv run streamlit run app/main.py
```

### Adding Dependencies
```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update dependencies
uv sync
```

## 🚀 Deployment

### Vercel Deployment
This application is designed to be deployed on Vercel:

1. **Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: PostgreSQL connection string (Vercel will provide)

2. **Build Configuration**
   - Vercel will automatically detect the Python application
   - Streamlit apps are supported on Vercel

3. **Deploy**
   ```bash
   vercel --prod
   ```

## 🎯 Use Cases

### For Tiger Team Members
1. **Case Creation**: Submit new critical cases via web form
2. **Research Phase**: AI analyzes customer history and product documentation
3. **Preparation**: Review AI recommendations before customer calls
4. **Case Management**: Track multiple cases and their progress

### For Support Managers
1. **Case Overview**: Monitor all active Tiger Team cases
2. **Resource Allocation**: View specialist availability and workload
3. **Performance Metrics**: Track case resolution times and success rates

## 🔮 Future Enhancements

- **Real-time Collaboration**: Multi-user case editing
- **Advanced Analytics**: Case pattern analysis and predictions
- **Integration**: Connect with IBM's internal support systems
- **Mobile App**: Native mobile application for field work
- **Voice Interface**: Voice-to-text for case notes and research

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support or questions about this system, please contact the development team.

---

**Built with ❤️ for IBM Tiger Teams**
