.PHONY: install dev-setup test format lint clean

install:
	pip install -e .

dev-setup:
	pip install -e ".[dev]"
	pip install pre-commit
	pre-commit install

test:
	pytest tests/ -v --cov=src/cloudscout --cov-report=html

format:
	black src/ tests/
	isort src/ tests/

lint:
	flake8 src/ tests/
	mypy src/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
