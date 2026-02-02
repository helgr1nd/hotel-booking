.PHONY: help install run test lint format clean docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies with Poetry"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make migrate      - Run Django migrations"
	@echo "  make clean        - Clean cache files"

install:
	poetry install

run:
	poetry run python manage.py runserver 9000

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .
	poetry run ruff check --fix .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

migrate:
	poetry run python manage.py migrate

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/
