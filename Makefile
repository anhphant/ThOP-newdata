# Makefile for THOP Algorithms: ACO, ACO++, BRKGA, ILS, SAASHC

.PHONY: all aco aco++ brkga ils saashc clean run-aco run-aco++ run-brkga run-ils run-saashc run-all help

# Compiler and flags
CXX = g++
CFLAGS = -O3 -fopenmp -std=c++11
PYTHON = python

help:
	@echo "THOP Algorithm Makefile"
	@echo "================================"
	@echo "Available targets:"
	@echo "  make all              - Build all algorithms"
	@echo "  make aco              - Build ACO"
	@echo "  make aco++            - Build ACO++"
	@echo "  make brkga            - Build BRKGA"
	@echo "  make ils              - Build ILS"
	@echo "  make saashc           - Build SAASHC"
	@echo ""
	@echo "  make run-aco          - Run ACO experiments"
	@echo "  make run-aco++        - Run ACO++ experiments"
	@echo "  make run-brkga        - Run BRKGA experiments"
	@echo "  make run-ils          - Run ILS experiments"
	@echo "  make run-saashc       - Run SAASHC experiments"
	@echo "  make run-all          - Run all algorithms"
	@echo ""
	@echo "  make clean            - Remove all compiled binaries"

# Build all algorithms
all: aco aco++ brkga ils saashc
	@echo "All algorithms built successfully!"

# ACO Build
aco:
	@echo "Building ACO..."
	cd src/aco && $(MAKE)
	@echo "ACO built successfully!"

# ACO++ Build
aco++:
	@echo "Building ACO++..."
	cd src/aco++ && $(MAKE)
	@echo "ACO++ built successfully!"

# BRKGA Build
brkga:
	@echo "Building BRKGA..."
	$(CXX) $(CFLAGS) src/brkga/brkga_main.cpp -o brkgathop
	@echo "BRKGA built successfully!"

# ILS Build
ils:
	@echo "Building ILS..."
	$(CXX) $(CFLAGS) src/ils/ils_main.cpp -o ilsthop
	@echo "ILS built successfully!"

# SAASHC Build
saashc:
	@echo "Building SAASHC..."
	cd src/saashc && cmake -B build && cmake --build build
	@echo "SAASHC built successfully!"

# Run experiments
run-aco: aco
	@echo "Running ACO experiments..."
	cd src/aco && $(PYTHON) run_all_experiments.py

run-aco++: aco++
	@echo "Running ACO++ experiments..."
	cd src/aco++ && $(PYTHON) run_aco++_experiments.py

run-brkga: brkga
	@echo "Running BRKGA experiments..."
	cd src/brkga && $(PYTHON) run_brkga_experiments.py

run-ils: ils
	@echo "Running ILS experiments..."
	cd src/ils && $(PYTHON) run_ils_experiments.py

run-saashc: saashc
	@echo "Running SAASHC experiments..."
	cd src/saashc && $(PYTHON) run_experiments.py

# Run all algorithms
run-all: run-aco run-aco++ run-brkga run-ils run-saashc
	@echo "All experiments completed!"

# Clean build artifacts
clean:
	@echo "Cleaning up..."
	rm -f brkgathop ilsthop
	cd src/aco && $(MAKE) clean || true
	cd src/aco++ && $(MAKE) clean || true
	cd src/saashc && rm -rf build || true
	@echo "Cleanup complete!"
