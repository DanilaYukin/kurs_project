import logging
import os

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info("Получение данных переменного окружения...")
load_dotenv()
API_KEY = os.getenv("API_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")
logger.info("Данные переменного окружения получены")


def currency_rate(currencies: list) -> list[dict]:
    """Функция обеспечивает обращение к внешнему API для получения текущего курса заданных валют"""

    logger.info(f"Функция currency_rate вызвана с параметрами {currencies}")
    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {"base": "RUB", "symbols": ",".join(currencies)}
    response = requests.get(url, params=params, headers={"apikey": API_KEY})

    if response.status_code != 200:
        logger.error(f"Нет ответа от {url}")
        raise requests.RequestException

    logger.info(f"Данные по курсам валют успешно получены от {url}")
    response_data = response.json()
    currency_rates = []
    for currency in currencies:
        currency_rates.append({"currency": currency, "rate": round(1 / response_data["rates"][currency], 2)})
    return currency_rates


def stocks_rate(stocks: list) -> list[dict]:
    """Функция обеспечивает обращение к внешнему API для получения текущих цен заданных акций"""

    logger.info(f"Функция stocks_rate вызвана с параметрами {stocks}")
    stocks_rates = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={STOCKS_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Нет ответа на запрос {url}")
            raise requests.RequestException
        logger.info(f"Получен ответ на запрос {url}")
        response_data = response.json()
        stocks_rates.append({"stock": stock, "price": round(float(response_data["Global Quote"]["05. price"]), 2)})
    return stocks_rates
