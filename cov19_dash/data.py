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


def fetch_latest_data() -> None:
    """Get global covid-19 data from the "Our World in Data" public GitHub
    repository.
    """
    print("Fetching latest data...")
    data = pd.read_csv(OWID_URL)

    # Switch column names to title case
    data.columns = [col.replace("_", " ").title() for col in data.columns]

    (
        # Remove regional totals: 'OWID_AFR', 'OWID_ASI', 'OWID_EUR',
        # 'OWID_EUN', 'OWID_INT', 'OWID_KOS', 'OWID_NAM', 'OWID_OCE',
        # 'OWID_SAM', 'OWID_WRL'
        data[~data["Iso Code"].str.startswith("OWID")]
        # Persist local copy
        .to_csv(DATA_DIR / "latest-data.csv", index=False)
    )


def fetch_jhu_data(category: str) -> pd.Series:
    """Get global covid-19 data for the given category from the JHU CSSE
    COVID-19 repository.

    Parameters
    ----------
    category : {"confirmed", "deaths"}
        The information to fetch.

    Returns
    -------
    pd.Series
        Data for the specified category.
    """
    data = pd.read_csv(f"{JHU_URL}_{category}_global.csv")

    data = (
        # Eliminate unnecessary columns
        data.drop(["Lat", "Long", "Province/State"], axis=1)
        # Get totals for each country. "Country/Region" becomes the index.
        .groupby("Country/Region").sum()
        # The columns now left are all dates. Renaming them labels them as
        # "Date" after pivoting the index.
        .rename_axis(columns="Date")
        # Pivot the index. This results in a Series with the category's data,
        # and a MultiIndex with "Country/Region" and "Date".
        .unstack()
        # Set the category as the Series' label.
        .rename(category.capitalize())
    )
    return data


def fetch_time_series_data() -> None:
    """Get "confirmed" and "deaths" information.

    Returns
    -------
    A pandas DataFrame with covid-19 case information.
    """
    print("Fetching time series info...")
    case_data = pd.concat(
        [fetch_jhu_data(category) for category in ("confirmed", "deaths")],
        axis=1,
    )

    # Restore "Country/Region" and "Date" index levels as columns, and set a
    # default RangeIndex
    case_data.reset_index(inplace=True)

    # Harmonize country names accross data sources
    case_data["Country/Region"] = case_data["Country/Region"].map(
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

    case_data.to_csv(DATA_DIR / "time-series-data.csv", index=False)


def load_latest_day_data() -> pd.DataFrame:
    """Get cleaned COVID-19 data for the latest day.

    Returns
    -------
    pandas.DataFrame
        COVID-19 info for the latest day.
    """
    return pd.read_csv(
        DATA_DIR / "latest-data.csv", parse_dates=["Last Updated Date"]
    )


def load_time_series_data() -> pd.DataFrame:
    """Get cleaned COVID-19 time series data.

    Returns
    -------
    pandas.DataFrame
        COVID-19 time series data.
    """
    return pd.read_csv(DATA_DIR / "time-series-data.csv", parse_dates=["Date"])
