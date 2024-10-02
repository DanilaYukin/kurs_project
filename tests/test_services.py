import pandas as pd

from src.services import filter_by_transaction_individual


def test_filter_by_transaction_individual():
    data = {
        'Категория': ['Переводы', 'Переводы', 'Еда', 'Переводы'],
        'Описание': ['Валерий А.', 'Сергей З.', 'Закупка продуктов', 'Алексей М.'],
        'Сумма': [1000, 2000, 500, 1500]
    }
    transactions = pd.DataFrame(data)

    expected_result = (
        '[{"Категория":"Переводы",'
        '"Описание":"Валерий А.",'
        '"Сумма":1000},'
        '{"Категория":"Переводы",'
        '"Описание":"Сергей З.",'
        '"Сумма":2000},'
        '{"Категория":'
        '"Переводы",'
        '"Описание":"Алексей М."'
        ',"Сумма":1500}]')

    result = filter_by_transaction_individual(transactions)

    assert result == expected_result
