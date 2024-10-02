import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import date_convert, open_xls, user_settings
from tests.conftest import dict_prepared, dict_raw


@pytest.fixture
def dict_for_pd_as_xls():
    return dict_raw


@pytest.fixture
def dict_for_pd_for_working():
    return dict_prepared


@patch("pandas.read_excel")
def test_get_transactions_from_xls(mock_read_excel, dict_for_pd_as_xls, dict_for_pd_for_working):
    m = mock_open()
    mock_read_excel.return_value = pd.DataFrame(dict_for_pd_as_xls)
    result = pd.DataFrame(dict_for_pd_for_working)
    with patch("builtins.open", m):
        assert result.equals(open_xls("test"))
        mock_read_excel.assert_called_once_with("test")


@pytest.mark.parametrize(
    "input_date, output_date",
    [
        ("21.01.2024", datetime.datetime.strptime("21.01.2024", "%d.%m.%Y")),
        ("21.01.2024 11:11:12", datetime.datetime.strptime("21.01.2024 11:11:12", "%d.%m.%Y %H:%M:%S")),
        ("2024-01-21 11:11:12", datetime.datetime.strptime("2024-01-21 11:11:12", "%Y-%m-%d %H:%M:%S")),
        ("2024-01", datetime.datetime.strptime("2024-01", "%Y-%m")),
    ],
)
def test_date_converter(input_date, output_date):
    assert date_convert(input_date) == output_date
    with pytest.raises(Exception) as ex:
        date_convert("invalid date")
    assert str(ex.value) == "Неверный формат даты"


def test_get_user_settings():
    m_open = mock_open(
        read_data="""
        {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }"""
    )
    user_settings()
    with patch("builtins.open", m_open):
        assert user_settings("test") == (["USD", "EUR"], ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
