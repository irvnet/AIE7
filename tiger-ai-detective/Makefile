.PHONY: help install setup run test format lint clean

help: ## Show this help message
	@echo "IBM Tiger Team Support System - Development Commands"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	@echo "🔄 Installing dependencies..."
	uv sync
	@echo "✅ Dependencies installed"

setup: ## Complete setup (install + database + mock data)
	@echo "🚀 Setting up IBM Tiger Team Support System..."
	uv sync
	@echo "🔄 Creating database tables..."
	uv run python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"
	@echo "🔄 Generating mock data..."
	uv run python scripts/generate_mock_data.py
	@echo "✅ Setup completed successfully!"

run: ## Run the Streamlit application
	@echo "🚀 Starting IBM Tiger Team Support System..."
	uv run streamlit run app/main.py --server.port 8501 --server.address localhost

test: ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	uv run black app/
	uv run isort app/

lint: ## Lint code with flake8
	@echo "🔍 Linting code..."
	uv run flake8 app/

typecheck: ## Run type checking with mypy
	@echo "🔍 Running type checks..."
	uv run mypy app/

check: format lint typecheck ## Run all code quality checks

clean: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__/
	rm -rf app/__pycache__/
	rm -rf app/*/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -f *.db
	rm -f tiger_team_support.db
	@echo "✅ Cleanup completed"

dev: ## Start development environment
	@echo "🚀 Starting development environment..."
	uv run streamlit run app/main.py --server.port 8501 --server.address localhost --server.runOnSave true

mock-data: ## Generate mock data
	@echo "🔄 Generating mock data..."
	uv run python scripts/generate_mock_data.py

db-reset: ## Reset database and regenerate mock data
	@echo "🔄 Resetting database..."
	rm -f *.db
	rm -f tiger_team_support.db
	uv run python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"
	uv run python scripts/generate_mock_data.py
	@echo "✅ Database reset completed"
