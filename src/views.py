import datetime as dt
import json
import logging

import pandas as pd

from external_api import currency_rate, stocks_rate
from utils import date_convert

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_current_month_data(transactions: pd.DataFrame, date: str) -> pd.DataFrame:
    """Возвращает данные за текущий месяц. Если дата — 20.05.2020,
    то данные для анализа будут в диапазоне 01.05.2020-20.05.2020
    """

    end_date = date_convert(date)
    start_date = end_date.replace(day=1)
    end_date = end_date.replace(hour=0, minute=0, second=0) + dt.timedelta(days=1)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True, errors="coerce")
    month_transactions = transactions.loc[
        (transactions["Дата операции"] <= end_date) & (transactions["Дата операции"] >= start_date)
    ]
    return month_transactions


def greetings():
    date_hour = dt.datetime.now().hour
    if 6 <= date_hour <= 12:
        return "Доброе утро"
    elif 12 < date_hour <= 16:
        return "Добрый день"
    elif 23 <= date_hour < 6:
        return "Доброй ночи"
    else:
        return "Доброй вечер"


def filtered_card_data(transactions: pd.DataFrame) -> list[dict]:
    """Возвращает сумму расходов и кешбека по картам"""
    logger.info("Функция filtered_card_data вызвана")

    card_data = (
        transactions.loc[transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )

    output_data = []
    for card_number, total_spent in card_data.items():
        output_data.append(
            {"last_digits": card_number, "total_spent": abs(total_spent), "cashback": abs(round(total_spent / 100, 2))}
        )

    return output_data


def filtered_top_five_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Возвращает топ-5 транзакций по сумме платежа"""

    logger.info("Функция filtered_top_five_transactions вызвана")
    top_five_transactions = (
        transactions.sort_values(by="Сумма платежа", ascending=False).iloc[:5].to_dict(orient="records")
    )
    top_transactions = []
    for transaction in top_five_transactions:
        top_transactions.append(
            {
                "date": transaction["Дата операции"].date().strftime("%d.%m.%Y"),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    return top_transactions


def get_main_page_data(
    transactions: pd.DataFrame | list, date_time: str, user_currencies: list, user_stocks: list
) -> str:
    """Функция, для страницы Главная, возвращающая приветствие, данные по картам за этот месяц,
    топ 5 операций за месяц, курсы валют и акций
    """

    logger.info(f"Функция get_main_page_data вызвана с параметрами {date_time}, {user_currencies}, {user_stocks}")
    greeting = greetings()
    if isinstance(transactions, list):
        raise Exception("Список транзакций пуст")
    transactions = get_current_month_data(transactions, date_time)
    cards_data = filtered_card_data(transactions)
    top_transactions = filtered_top_five_transactions(transactions)
    currencies = currency_rate(user_currencies)
    stocks = stocks_rate(user_stocks)

    output_json = json.dumps(
        {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": currencies,
            "stock_prices": stocks,
        },
        indent=4,
        ensure_ascii=False,
    )

    return output_json
