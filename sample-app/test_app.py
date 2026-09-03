from app import stress_cpu, stress_memory, estimate_pi_monte_carlo
import os
import sys
import pytest
sys.path.insert(0, os.path.dirname(__file__))

# --- 1. HAPPY CASES


def test_estimate_pi_monte_carlo_happy_case():
    """Test range of π with lagre positive numbers"""
    assert 3.10 <= estimate_pi_monte_carlo(10000000) <= 3.18
    assert 3.13 <= estimate_pi_monte_carlo(3140000) <= 3.15
# --- 2. EDGE CASES & ERROR HANDLING


def test_estimate_pi_monte_carlo_edge_case():
    """Test range of π with 0 and negative numbers"""
    with pytest.raises(ValueError):
        estimate_pi_monte_carlo(-10000)
    with pytest.raises(ValueError):
        estimate_pi_monte_carlo(0)


def test_stress_cpu():
    """Test CPU stress function runs for the expected duration."""
    assert stress_cpu(0.2) >= 0.2


def test_stress_memory():
    """Test memory allocation function returns allocations MB"""
    assert stress_memory(10) == 10
