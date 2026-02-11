.PHONY: help install dev test lint migrate run docker-build docker-up clean

help:  ## Show this help message
	@grep -E "^[a-zA-Z_-]+:.*?## .*$$" $(MAKEFILE_LIST) | sort | \
		awk "BEGIN {FS = \":.*?## \"}; {printf \"\033[36m%-20s\033[0m %s\n\", $$1, $$2}"

install:  ## Install production dependencies
	pip install -r requirements.txt

dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov httpx black flake8 mypy

test:  ## Run test suite with coverage
	pytest tests/ -v --cov=app --cov-report=term-missing

lint:  ## Run linters
	black --check app/ tests/
	flake8 app/ tests/ --max-line-length=100
	mypy app/ --ignore-missing-imports

format:  ## Format code with black
	black app/ tests/

migrate:  ## Run database migrations
	alembic upgrade head

migrate-create:  ## Create new migration (usage: make migrate-create MSG="description")
	alembic revision --autogenerate -m "$(MSG)"

run:  ## Start development server
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-prod:  ## Start production server
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build:  ## Build Docker image
	docker-compose build

docker-up:  ## Start all services with Docker
	docker-compose up -d

docker-down:  ## Stop all Docker services
	docker-compose down

clean:  ## Clean up cache and build files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov