from unittest.mock import patch

import pytest

from src.external_api import currency_rate, stocks_rate


def test_currency_rate():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"base": "RUB", "rates": {"USD": 0.01, "EUR": 0.01}}
        assert currency_rate(["USD", "EUR"]) == [
            {"currency": "USD", "rate": 100.0},
            {"currency": "EUR", "rate": 100.0},
        ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 201
        with pytest.raises(Exception):
            assert currency_rate(["USD", "EUR"])


def test_stocks_rate():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"Global Quote": {"05. price": "230.5400"}}
        assert stocks_rate(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == [
            {"stock": "AAPL", "price": 230.5400},
            {"stock": "AMZN", "price": 230.5400},
            {"stock": "GOOGL", "price": 230.5400},
            {"stock": "MSFT", "price": 230.5400},
            {"stock": "TSLA", "price": 230.5400},
        ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 201
        with pytest.raises(Exception):
            assert stocks_rate(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
