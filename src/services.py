import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def filter_by_transaction_individual(transactions: pd.DataFrame):
    logger.info("Вызвана функция filter_by_transaction_individual")

    pattern = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ]\.$"

    filtered_transactions = transactions[
        (transactions["Категория"] == "Переводы") & transactions["Описание"].str.fullmatch(pattern)
    ]

    return filtered_transactions.to_json(orient="records", force_ascii=False)
