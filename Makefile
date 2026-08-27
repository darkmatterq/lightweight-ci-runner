CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip
SRC_DIR = src
BIN_DIR = bin

.PHONY: build test clean lint install-deps venv help

help:
	@echo "help: show this help message"
	@echo ".PHONY: all build test clean lint install-deps help"
	@echo "venv: install virtual environment"
	@echo "install-deps: install all packages in requirements.txt"
	@echo "build: compile C++ performance monitor binary"
	@echo "lint: check python code style and formatting"
	@echo "test: run all unit tests using pytest"
	@echo "clean: remove build artifacts and cache files"
	
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
clean:
	rm -rf __pycache__ .pytest_cache *.pyc
	rm -rf $(BIN_DIR)/*
