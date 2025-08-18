# 🚀 Quick Start Guide

Get the IBM Tiger Team Support System running in 5 minutes!

## Prerequisites

- Python 3.12+
- uv (Python package manager)
- OpenAI API key

## ⚡ Super Quick Start

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd ibm-tiger-team-support
   make setup
   ```

3. **Run the application**
   ```bash
   make run
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

5. **Initialize the system**
   - Enter your OpenAI API key in the sidebar
   - Click "Initialize System"
   - Start creating Tiger Team cases!

## 🎯 What You Can Do

### Create a New Case
1. Go to the "Create Case" tab
2. Fill out the case form:
   - Select customer and IBM product
   - Choose priority and assign team member
   - Describe the issue and desired outcome
3. Click "Create Case & Generate AI Research"
4. Review AI-generated recommendations

### Use the Research Assistant
1. Go to the "Research Assistant" tab
2. Ask questions like:
   - "How do I troubleshoot WebSphere memory leaks?"
   - "What are common Db2 performance issues?"
   - "What's the best approach for cluster communication failures?"
3. Get AI-powered research and recommendations

### View Active Cases
1. Go to the "View Cases" tab
2. See all active Tiger Team cases
3. Click on cases to view details and AI recommendations

## 🔧 Development Commands

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Reset database
make db-reset

# Development mode (auto-reload)
make dev
```

## 📊 Mock Data Included

The system comes with realistic mock data:
- **50+ Customers** (various industries)
- **8 IBM Products** (WebSphere, Db2, MQ, etc.)
- **15 Tiger Team Members** (different expertise)
- **200+ Support Tickets** (realistic issues)
- **30+ Active Cases** (with research notes)

## 🆘 Troubleshooting

### Common Issues

**"uv not found"**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**"OpenAI API key error"**
- Make sure you have a valid OpenAI API key
- Enter it in the Streamlit sidebar

**"Database error"**
```bash
make db-reset
```

**"Import errors"**
```bash
make clean
make setup
```

### Getting Help

1. Run the system test: `python test_system.py`
2. Check the logs in the Streamlit interface
3. Review the full README.md for detailed documentation

## 🎉 You're Ready!

Your IBM Tiger Team Support System is now running! Start creating cases and exploring the AI-powered research capabilities.
