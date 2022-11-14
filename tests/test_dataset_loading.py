from pandas import DataFrame, DatetimeIndex
from pandas.api.types import is_datetime64_dtype

from covid19_dash.data import (
    load_30_day_diff,
    load_latest_day_data,
    load_time_series_data,
)


def test_load_daily_diff():
    diff = load_30_day_diff()

    assert isinstance(diff, DataFrame)
    assert isinstance(diff.index, DatetimeIndex)
    assert diff.columns.to_list() == ["Confirmed", "Deaths"]
    assert diff.shape == (30, 2)


def test_load_time_Series_data():
    ts_data = load_time_series_data()

    assert isinstance(ts_data, DataFrame)
    assert ts_data.columns.to_list() == [
        "Date",
        "Country/Region",
        "Confirmed",
        "Deaths",
    ]
    assert is_datetime64_dtype(ts_data["Date"])


def test_load_latest_day_data():
    latest_day_data = load_latest_day_data()
    assert isinstance(latest_day_data, DataFrame)

    necessary_cols = [
        "Aged 70 Older",
        "Diabetes Prevalence",
        "Hospital Beds Per Thousand",
        "Life Expectancy",
        "New Cases",
        "People Fully Vaccinated",
        "People Fully Vaccinated Per Hundred",
        "Population Density",
        "Total Cases",
        "Total Cases Per Million",
        "Total Deaths",
        "Total Deaths Per Million",
        "Total Vaccinations",
    ]
    cols_set = set(latest_day_data.columns)
    for col in necessary_cols:
        assert col in cols_set
