"""
Example unit tests to demonstrate unit testing structure.
"""
import pytest
import numpy as np


@pytest.mark.unit
def test_example_unit_test():
    """Example unit test to verify unit test directory structure."""
    assert 1 + 1 == 2


@pytest.mark.unit
def test_financial_calculation_example():
    """Example financial calculation unit test."""
    principal = 1000
    rate = 0.05
    time = 2
    
    # Simple interest calculation
    simple_interest = principal * rate * time
    assert simple_interest == 100.0
    
    # Compound interest calculation
    compound_amount = principal * (1 + rate) ** time
    assert abs(compound_amount - 1102.5) < 0.01


@pytest.mark.unit
def test_array_operations():
    """Test array operations for financial data."""
    prices = np.array([100, 101, 99, 102, 98])
    returns = np.diff(prices) / prices[:-1]
    
    assert len(returns) == 4
    assert abs(returns[0] - 0.01) < 0.001  # (101-100)/100 = 0.01