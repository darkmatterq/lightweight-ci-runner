from app import is_even, is_prime, format_email
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# --- 1. HAPPY CASES


def test_is_even_happy_case():
    """Test even and odd numbers with valid inputs."""
    assert is_even(4) == "'4' is even"
    assert is_even(3) == "'3' is odd"


def test_is_prime_happy_case():
    """Test prime numbers with valid inputs."""
    assert is_prime(2) is True
    assert is_prime(7) is True
    assert is_prime(4) is False


def test_format_email_happy_case():
    """Test email validation with correct formats."""
    assert format_email("quan.ledinh@gmail.com") is True
    assert format_email("le.dinh.quan@uit.edu.vn") is True


# --- 2. EDGE CASES & ERROR HANDLING

def test_is_prime_edge_cases():
    """Test prime function with edge values like 0, 1, or negative numbers."""
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False


def test_format_email_edge_cases():
    """Test email validation with incorrect or messy formats."""
    assert format_email("quan@gmail") is False
    assert format_email("le dinh quan@uit.edu.vn") is False
    assert format_email("kdq#2006@yahoo.com") is False
