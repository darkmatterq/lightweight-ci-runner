CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3
PYTHON = python3
SRC_DIR = src
BIN_DIR = bin
.PHONY: all build test clean lint install-deps
help:
	@echo "help: show this help message"
	@echo ".PHONY: all build test clean lint install-deps help"
	@echo "install-deps: install all packages in requirements.txt"
	@echo "build: compile C++ performance monitor binary"
	@echo "lint: check python code style and formatting"
	@echo "test: run all unit tests using pytest"
	@echo "clean: remove build artifacts and cache files"
	
install-deps:
	$(PYTHON) -m pip install -r requirements.txt
build:
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/monitor.cpp -o $(BIN_DIR)/ci-monitor
lint:
	flake8 $(SRC_DIR) sample-app/
test:
	pytest
clean:
	rm -rf __pycache__ .pytest_cache *.pyc
	rm -rf $(BIN_DIR)/*
