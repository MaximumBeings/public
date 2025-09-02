"""
Example integration tests to demonstrate integration testing structure.
"""
import pytest
import pandas as pd
import numpy as np


@pytest.mark.integration
def test_example_integration_test(sample_dataframe):
    """Example integration test to verify integration test directory structure."""
    df = sample_dataframe
    
    # Test data processing pipeline
    df['returns'] = df['price'].pct_change()
    df['ma_5'] = df['price'].rolling(window=5).mean()
    df['volatility'] = df['returns'].rolling(window=5).std()
    
    assert 'returns' in df.columns
    assert 'ma_5' in df.columns
    assert 'volatility' in df.columns


@pytest.mark.integration
def test_data_pipeline_integration(sample_csv_file):
    """Test integration between file I/O and data processing."""
    # Read data from file
    df = pd.read_csv(sample_csv_file)
    
    # Process data
    df['price_normalized'] = df['price'] / df['price'].iloc[0]
    df['volume_ma'] = df['volume'].rolling(window=2).mean()
    
    # Verify integration
    assert len(df) > 0
    assert df['price_normalized'].iloc[0] == 1.0
    assert not df['volume_ma'].iloc[1:].isna().any()


@pytest.mark.integration
@pytest.mark.slow
def test_complex_calculation_integration(mock_market_data):
    """Test integration of multiple calculation components."""
    rates = mock_market_data['rates']
    
    # Simulate a complex calculation involving multiple components
    yield_curve = list(rates.values())
    
    # Calculate some derived metrics
    avg_rate = np.mean(yield_curve)
    rate_spread = max(yield_curve) - min(yield_curve)
    
    assert avg_rate > 0
    assert rate_spread > 0
    assert len(yield_curve) == len(rates)