import datetime as dt
import logging
from typing import Callable

import pandas as pd

from utils import date_convert

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def save_report_to_file(file_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(str(result))

            return result

        return wrapper

    return decorator


@save_report_to_file("report.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> pd.DataFrame:
    """Функция для формирования трат по заданной категории за три месяца от заданной даты"""
    logger.info(f"Запущено формирование отчета spending_by_category с параметрами {category}, {date}")
    if date is None:
        date_end = dt.datetime.now()
    else:
        date_end = date_convert(date)

    date_start = date_end - dt.timedelta(days=90)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True, errors="coerce")
    transactions_by_category = transactions.loc[
        (transactions["Дата операции"] <= date_end)
        & (transactions["Дата операции"] >= date_start)
        & (transactions["Категория"] == category)
    ]
    logger.info(f"Отчет сформирован с параметрами {category}, {date_start}, {date_end}")
    return transactions_by_category
