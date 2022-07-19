from datetime import date
from functools import lru_cache
from pathlib import Path

import pandas as pd

OWID_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/"
    "latest/owid-covid-latest.csv"
)
JHU_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_"
    "covid_19_data/csse_covid_19_time_series/time_series_covid19"
)
DATA_DIR = Path("covid-19-data")
DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_URL = (
    "https://raw.githubusercontent.com/Tim-Abwao/covid19-global-dashboard/"
    "main/covid-19-data"
)
TODAY = date.today()


def fetch_latest_data() -> None:
    """Get COVID-19 data from the "Our World in Data" public GitHub repo."""
    print("Fetching latest data...")
    data = pd.read_csv(OWID_URL)

    # Switch column names to title case
    data.columns = data.columns.str.replace("_", " ").str.title()

    (
        # Remove regional totals: 'OWID_AFR', 'OWID_ASI', 'OWID_EUR',
        # 'OWID_EUN', 'OWID_INT', 'OWID_KOS', 'OWID_NAM', 'OWID_OCE',
        # 'OWID_SAM', 'OWID_WRL'
        data[~data["Iso Code"].str.startswith("OWID")]
        # Persist local copy
        .to_csv(DATA_DIR / "latest-data.csv", index=False)
    )


def fetch_jhu_data(category: str) -> pd.Series:
    """Get global covid-19 data for the given `category` from the JHU CSSE
    COVID-19 repository.

    Args:
        category (str): The information to fetch.

    Returns:
        pandas.Series: Data for the specified category.
    """
    data = pd.read_csv(f"{JHU_URL}_{category}_global.csv")
    data = (
        # Eliminate unnecessary columns
        data.drop(["Lat", "Long", "Province/State"], axis=1)
        # Get totals for each country
        .groupby("Country/Region").sum()
        # Remaining columns are all dates
        .rename_axis(columns="Date")
        # Pivot the index. This results in a Series with a MultiIndex having
        # "Country/Region" and "Date".
        .unstack()
        # Set the category as the Series' label.
        .rename(category.capitalize())
    )
    return data


def fetch_time_series_data() -> None:
    """Get "confirmed" and "deaths" info from JHU CSSE."""
    print("Fetching time series info...")
    case_data = pd.concat(
        [fetch_jhu_data(category) for category in ("confirmed", "deaths")],
        axis=1,
    )
    # Restore "Country/Region" and "Date" index levels as columns
    case_data.reset_index(inplace=True)

    # Harmonize country names accross data sources
    case_data["Country/Region"] = case_data["Country/Region"].replace(
        {
            "Cabo Verde": "Cape Verde",
            "Congo (Brazzaville)": "Congo",
            "Congo (Kinshasa)": "Democratic Republic of Congo",
            "Micronesia": "Micronesia (country)",
            "Burma": "Myanmar",
            "West Bank and Gaza": "Palestine",
            "Korea, South": "South Korea",
            "Taiwan*": "Taiwan",
            "Timor-Leste": "Timor",
            "US": "United States",
            "Holy See": "Vatican",
        }
    )
    case_data["Date"] = pd.to_datetime(case_data["Date"])

    # Save last 30 daily differences
    case_data.groupby("Date").sum().diff().tail(30).to_csv(
        DATA_DIR / "daily-differences.csv"
    )
    # Aggregate weekly to reduce file size. Select values at start of week.
    case_data.groupby("Country/Region").resample(
        "1W", on="Date"
    ).first().to_csv(DATA_DIR / "time-series-data.csv", index=False)


@lru_cache(maxsize=2)
def load_latest_day_data(date: date = TODAY) -> pd.DataFrame:
    """Get cleaned COVID-19 data for the latest day.

    Args:
        date (date): The current date.

    Returns:
        pandas.DataFrame: COVID-19 info for the latest day.
    """
    return pd.read_csv(
        f"{PROCESSED_DATA_URL}/latest-data.csv",
        parse_dates=["Last Updated Date"],
    )


@lru_cache(maxsize=2)
def load_time_series_data(date: date = TODAY) -> pd.DataFrame:
    """Get cleaned COVID-19 time series data.

    Args:
        date (date): The current date.

    Returns:
        pandas.DataFrame: COVID-19 time series data.
    """
    return pd.read_csv(
        f"{PROCESSED_DATA_URL}/time-series-data.csv", parse_dates=["Date"]
    )


@lru_cache(maxsize=2)
def load_30_day_diff(date: date = TODAY) -> pd.DataFrame:
    """Get daily differences for the last 30 days..

    Args:
        date (date): The current date.

    Returns:
        pandas.DataFrame: Daily changes for last 30 days.
    """
    return pd.read_csv(
        f"{PROCESSED_DATA_URL}/daily-differences.csv", parse_dates=[0]
    ).set_index("Date")


if __name__ == "__main__":
    fetch_latest_data()
    fetch_time_series_data()
