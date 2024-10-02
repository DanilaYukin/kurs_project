import pandas as pd
import pytest

from src.reports import spending_by_category
from tests.conftest import dict_prepared


@pytest.fixture
def input_dataframe():
    return pd.DataFrame(dict_prepared)


def test_get_cashback_by_category(input_dataframe):
    assert spending_by_category(input_dataframe, "Супермаркеты", "31.12.2021") is None
