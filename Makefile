CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip
SRC_DIR = src
BIN_DIR = bin

.PHONY: all help venv install-deps build test lint run clean clean-docker clean-all

help:
	@echo "Lightweight CI Runner - Makefile Commands:"
	@echo "make venv             - Create Python virtual environment"
	@echo "make install-deps     - Install dependencies from requirements.txt"
	@echo "make build            - Compile C++ performance monitor binary"
	@echo "make test             - Run unit tests using pytest"
	@echo "make lint             - Check Python code style (flake8)"
	@echo "make run              - Run full CI/CD pipeline end-to-end"
	@echo "make clean            - Clean all binary builds and Python bytecode/cache"
	@echo "make clean-docker     - Clean dangling Docker containers and images"
	@echo "make clean-all        - Deep clean everything including .venv"


venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
	echo "Creating isolated Python virtual environment (.venv)..."; \
	python3 -m venv $(VENV_DIR); \
	fi
install-deps: venv
	$(PIP) install -r requirements.txt
build:
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/monitor.cpp -o $(BIN_DIR)/ci-monitor
lint: venv
	$(VENV_DIR)/bin/flake8 $(SRC_DIR) sample-app/
test: venv
	$(VENV_DIR)/bin/pytest
run: build venv
	$(PYTHON) ${SRC_DIR}/engine.py sample-app/.ci-pipeline.yaml
clean:
	@echo "Cleaning build artifacts and python caches..."

	rm -rf $(BIN_DIR)/*
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null ||true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

	@echo "Workspace is clean"
clean-docker:
	./scripts/cleanup.sh
clean-all: clean clean-docker
	@echo "Removing virtual environment (.venv)..."
	rm -rf $(VENV_DIR)
	@echo "Deep clean completed!"

	


