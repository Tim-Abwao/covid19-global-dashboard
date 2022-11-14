from pandas import MultiIndex, Series

from covid19_dash import data as data_module
from covid19_dash.data import (
    fetch_jhu_data,
    fetch_latest_data,
    fetch_time_series_data,
)


def test_fetch_jhu_data():
    confirmed_cases = fetch_jhu_data(category="confirmed")

    assert isinstance(confirmed_cases, Series)
    assert confirmed_cases.name == "Confirmed"
    assert isinstance(confirmed_cases.index, MultiIndex)


def test_fetch_latest_owid_data(monkeypatch, temp_data_dir, capsys):
    # Overwrite default data location
    monkeypatch.setattr(data_module, "DATA_DIR", temp_data_dir)

    expected_file = temp_data_dir / "latest-data.csv"
    expected_file.unlink(missing_ok=True)  # Make sure file doesn't exists

    fetch_latest_data()
    captured = capsys.readouterr()
    assert "Fetching latest data..." in captured.out
    assert expected_file.is_file()


def test_fetch_time_series_data(monkeypatch, temp_data_dir, capsys):
    # Overwrite default data location
    monkeypatch.setattr(data_module, "DATA_DIR", temp_data_dir)

    expected_daily_diff = temp_data_dir / "daily-differences.csv"
    expected_ts = temp_data_dir / "time-series-data.csv"
    # Make sure files don't already exists
    expected_daily_diff.unlink(missing_ok=True)
    expected_ts.unlink(missing_ok=True)

    fetch_time_series_data()
    captured = capsys.readouterr()
    assert "Fetching time series info..." in captured.out
    assert expected_daily_diff.is_file()
    assert expected_ts.is_file()