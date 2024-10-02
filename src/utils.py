import datetime
import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def open_xls(path: str):
    """Функция открывает excel файл и возвращает словарь"""
    logger.info(f"Вызвана функция получения транзакций из файла {open_xls}")
    operations = pd.read_excel(path)
    return operations


def date_convert(date: str) -> datetime.datetime:
    """Функция которая ковертирует дату"""
    logger.info(f"Вызвана функция распознавания и конвертации даты {date}")
    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y")
        logger.info("Дата в формате %d.%m.%Y успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        logger.info("Дата в формате %d.%m.%Y %H:%M:%S успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        logger.info("Дата в формате %Y-%m-%d %H:%M:%S успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        pass

    try:
        date_dt = datetime.datetime.strptime(date, "%Y-%m")
        logger.info("Дата в формате %Y-%m успешно получена")
        return date_dt

    except (NameError, TypeError, ValueError):
        logger.error("Неверный формат даты")
        pass

    raise Exception("Неверный формат даты")


def user_settings(path: str = "user_settings.json") -> tuple:
    """Возвращает список валют и список акций из json с настройками пользователя"""

    logger.info(f"Вызвана функция получения настроек пользователя из {path}")
    with open(path) as file:
        user_settings = json.load(file)
        logger.info("Успешно получены настройки пользователя")
    return user_settings["user_currencies"], user_settings["user_stocks"]
