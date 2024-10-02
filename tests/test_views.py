import json
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import (
    filtered_card_data,
    filtered_top_five_transactions,
    get_current_month_data,
    greetings,
    get_main_page_data,
)
from tests.conftest import dict_prepared, top_five_transactions


@pytest.fixture
def input_dataframe():
    return pd.DataFrame(dict_prepared)


@pytest.fixture
def top_five():
    return top_five_transactions


def test_get_current_month_data(input_dataframe):
    assert input_dataframe.equals(get_current_month_data(input_dataframe, "31.12.2021"))


def test_filtered_top_five_transactions(input_dataframe, top_five):
    assert filtered_top_five_transactions(input_dataframe) == top_five


@pytest.mark.parametrize(
    "hour, greeting", [(1, "Доброй ночи"), (6, "Доброе утро"), (13, "Добрый день"), (17, "Добрый вечер")]
)
def test_get_greeting(hour, greeting):
    with patch("datetime.datetime") as mock_datetime:
        mock_now = datetime(2024, 7, 13, hour, 0, 0)
        mock_datetime.now.return_value = mock_now
        assert greetings() == greeting


def test_filtered_card_data(input_dataframe):
    assert filtered_card_data(input_dataframe) == [
        {"last_digits": "*5091", "total_spent": 564.0, "cashback": 5.64},
        {"last_digits": "*7197", "total_spent": 421.06, "cashback": 4.21},
    ]


def test_get_main_page_data(input_dataframe, top_five):
    with patch("src.views.get_greeting") as mock_get_greeting:
        mock_get_greeting.return_value = "Добрый день"
        with pytest.raises(Exception) as ex:
            get_main_page_data([], "11.11.2023", [1, 2], [1, 2])
        assert str(ex.value) == "Список транзакций пуст"

    with patch("src.views.get_greeting") as mock_get_greeting:
        mock_get_greeting.return_value = "Добрый день"
        with patch("src.views.get_current_month_data") as mock_get_current_month_data:
            mock_get_current_month_data.return_value = input_dataframe
            with patch("src.views.filtered_card_data") as mock_filtered_card_data:
                mock_filtered_card_data.return_value = [
                    {"last_digits": "*5091", "total_spent": 564.0, "cashback": 5.64},
                    {"last_digits": "*7197", "total_spent": 421.06, "cashback": 4.21},
                ]
                with patch("src.views.filtered_top_five_transactions") as mock_filtered_top_five_transactions:
                    mock_filtered_top_five_transactions.return_value = top_five
                    with patch("src.views.currency_rate") as mock_currency_rate:
                        mock_currency_rate.return_value = []
                        with patch("src.views.stocks_rate") as mock_stocks_rate:
                            mock_stocks_rate.return_value = []
                            assert get_main_page_data(input_dataframe, "11.11.2023", [1, 2], [1, 2]) == json.dumps(
                                {
                                    "greeting": "Добрый день",
                                    "cards": [
                                        {"last_digits": "*5091", "total_spent": 564.0, "cashback": 5.64},
                                        {"last_digits": "*7197", "total_spent": 421.06, "cashback": 4.21},
                                    ],
                                    "top_transactions": top_five,
                                    "currency_rates": [],
                                    "stock_prices": [],
                                },
                                indent=4,
                                ensure_ascii=False,
                            )
