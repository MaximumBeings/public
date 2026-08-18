import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing."""
    csv_path = temp_dir / "sample_data.csv"
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'price': [100.0, 101.5, 99.8],
        'volume': [1000, 1200, 800]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_dataframe():
    """Create a sample pandas DataFrame for testing."""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    return pd.DataFrame({
        'date': dates,
        'price': np.random.uniform(90, 110, 10),
        'volume': np.random.randint(500, 2000, 10),
        'returns': np.random.normal(0, 0.02, 10)
    })


@pytest.fixture
def mock_quantlib():
    """Mock QuantLib objects for testing."""
    mock = MagicMock()
    mock.Date.return_value = Mock()
    mock.Settings.instance.return_value.evaluationDate = Mock()
    mock.Actual365Fixed.return_value = Mock()
    mock.TARGET.return_value = Mock()
    return mock


@pytest.fixture
def sample_bond_data():
    """Sample bond data for testing bond calculations."""
    return {
        'face_value': 1000.0,
        'coupon_rate': 0.05,
        'maturity_years': 5,
        'yield_rate': 0.04,
        'payment_frequency': 2
    }


@pytest.fixture
def sample_option_data():
    """Sample option data for testing options calculations."""
    return {
        'spot_price': 100.0,
        'strike_price': 105.0,
        'time_to_expiry': 0.25,
        'risk_free_rate': 0.03,
        'volatility': 0.20,
        'option_type': 'call'
    }


@pytest.fixture
def sample_swap_data():
    """Sample swap data for testing swap calculations."""
    return {
        'notional': 1000000.0,
        'fixed_rate': 0.025,
        'floating_spread': 0.001,
        'tenor_years': 5,
        'payment_frequency': 4
    }


@pytest.fixture
def mock_market_data():
    """Mock market data for testing."""
    return {
        'rates': {
            '1M': 0.015,
            '3M': 0.018,
            '6M': 0.022,
            '1Y': 0.025,
            '2Y': 0.028,
            '5Y': 0.032,
            '10Y': 0.035
        },
        'fx_rates': {
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'USDJPY': 148.50
        },
        'equity_prices': {
            'SPY': 450.25,
            'QQQ': 375.80,
            'IWM': 185.40
        }
    }


@pytest.fixture
def mock_http_response():
    """Mock HTTP response for testing web scraping functions."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
    <html>
        <body>
            <table>
                <tr><th>Symbol</th><th>Price</th></tr>
                <tr><td>AAPL</td><td>150.00</td></tr>
                <tr><td>GOOGL</td><td>2500.00</td></tr>
            </table>
        </body>
    </html>
    """
    mock_response.json.return_value = {
        'data': [
            {'symbol': 'AAPL', 'price': 150.00},
            {'symbol': 'GOOGL', 'price': 2500.00}
        ]
    }
    return mock_response


@pytest.fixture
def sample_time_series():
    """Create a sample time series for testing."""
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    prices = 100 * np.exp(np.cumsum(np.random.normal(0, 0.01, len(dates))))
    return pd.Series(prices, index=dates, name='price')


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'test_db'
        },
        'api': {
            'base_url': 'https://api.test.com',
            'timeout': 30
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }


@pytest.fixture
def sample_yield_curve():
    """Sample yield curve data for testing."""
    maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    rates = [0.015, 0.018, 0.022, 0.025, 0.028, 0.032, 0.035, 0.038, 0.042, 0.045]
    return dict(zip(maturities, rates))


@pytest.fixture
def mock_database_connection():
    """Mock database connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('AAPL', 150.00, '2023-12-01'),
        ('GOOGL', 2500.00, '2023-12-01')
    ]
    mock_cursor.fetchone.return_value = ('AAPL', 150.00, '2023-12-01')
    return mock_conn


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing."""
    return {
        'assets': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
        'weights': [0.3, 0.25, 0.25, 0.2],
        'prices': [150.00, 2500.00, 300.00, 200.00],
        'quantities': [100, 10, 50, 25]
    }


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducibility."""
    np.random.seed(42)


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print statements."""
    from io import StringIO
    import sys
    
    fake_stdout = StringIO()
    monkeypatch.setattr(sys, 'stdout', fake_stdout)
    return fake_stdout


@pytest.fixture
def mock_external_api():
    """Mock external API responses for testing."""
    mock_api = Mock()
    mock_api.get_stock_price.return_value = 150.00
    mock_api.get_fx_rate.return_value = 1.0850
    mock_api.get_yield_curve.return_value = {
        '1Y': 0.025,
        '5Y': 0.032,
        '10Y': 0.035
    }
    return mock_api