.PHONY: install test lint format clean help run-example

help:
	@echo "AI Code Generator - Available Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean generated files"
	@echo "  make run-example  - Run example generation (without GitHub push)"
	@echo "  make help         - Show this help message"

install:
	pip install -r requirements.txt

test:
	pytest --cov=src --cov-report=term-missing --cov-report=html -v

lint:
	pylint src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf generated_projects/*

run-example:
	python -m src.main -d "Build a REST API for todo management" -n "demo-todo-api" --skip-github

generate-nodejs:
	python -m src.main -d "Build a Node.js REST API" -t "nodejs-express" --skip-github

generate-python:
	python -m src.main -d "Build a Python FastAPI" -t "python-fastapi" --skip-github

generate-react:
	python -m src.main -d "Build a React dashboard" -t "react-typescript" --skip-github

generate-cli:
	python -m src.main -d "Build a CLI tool" -t "python-cli" --skip-github
