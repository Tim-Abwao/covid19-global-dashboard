import pandas as pd
from pathlib import Path


BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'\
    'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19'


data_dir = Path('data')
location_data = pd.read_csv(data_dir.joinpath('location_data.csv'))


def fetch_data(category='confirmed'):
    """Get global covid-19 data for the given category from the JHU CSSE
    COVID-19 repository.

    Parameters
    ----------
    category: {'confirmed', 'deaths', 'recovered'}
        The information to fetch.
    """
    data = pd.read_csv(f'{BASE_URL}_{category}_global.csv')

    data = (
        # Eliminate unnecessary columns
        data.drop(['Lat', 'Long', 'Province/State'], axis=1)
        # Get totals for each country. 'Country/Region' becomes the index.
        .groupby('Country/Region').sum()
        # The columns now left are all dates. Renaming them labels them as
        # 'Date' after pivoting the index.
        .rename_axis(columns='Date')
        # Pivot the index. This results in a Series with the category's data,
        # and a MultiIndex with 'Country/Region' and 'Date'.
        .unstack()
        # Ensure all values are positive
        .clip(lower=0)
        # Set the category as the Series' label.
        .rename(category.capitalize())
    )

    return data


def get_case_information():
    """Get combined 'confirmed', 'deaths' and 'recovered' case information.
    Then calculate 'active' cases.

    Returns
    -------
    A pandas DataFrame with covid-19 case information.
    """
    case_data = [fetch_data(category)
                 for category in {'confirmed', 'deaths', 'recovered'}]
    case_data_df = (
        # Combine the case data into a DataFrame
        pd.concat(case_data, axis=1)
        # Restore 'Country/Region' and 'Date' as columns and set a default
        # RangeIndex
        .reset_index()
    )
    # Convert the dates to datetime format
    case_data_df['Date'] = pd.to_datetime(case_data_df['Date'])

    # Calculate active cases
    case_data_df['Active'] = (case_data_df['Confirmed']
                              - case_data_df['Recovered']
                              - case_data_df['Deaths'])
    return case_data_df


def refresh_datasets():
    """Save fresh copies of the data used in the dashboard.
    """
    case_data = get_case_information()

    # Save daily time series
    daily_values_file = data_dir.joinpath('daily_values.csv')
    case_data.to_csv(daily_values_file, index=False)

    # Save latest day's data
    latest_day_file = data_dir.joinpath('latest_day.csv')
    (case_data
     .query("Date == @case_data['Date'].max()")  # Select latest day's data
     .to_csv(latest_day_file, index=False))


def load_latest_day_data():
    """Get data for the latest day, and include location data.

    Returns
    -------
    A pandas DataFrame with 'confirmed', 'active', 'recovered' and 'deaths'
    info for the latest day.
    """
    file = data_dir.joinpath('latest_day.csv')
    if file.exists():
        data = pd.read_csv(file, parse_dates=['Date'])
        return data.merge(location_data)
    else:
        print('Downloading data...')
        refresh_datasets()
        return load_latest_day_data()


def load_time_series_data():
    """Get daily time series data.

    Returns
    -------
    A pandas DataFrame with 'confirmed', 'recovered' and 'deaths' info over a
    range of dates.
    """
    file = data_dir.joinpath('daily_values.csv')
    if file.exists():
        return pd.read_csv(file, parse_dates=['Date'])
    else:
        print('Downloading data...')
        refresh_datasets()
        return load_time_series_data()


def check_if_data_is_stale():
    """Scan current files, and create fresh copies if they are missing or
    outdated.
    """
    file = data_dir.joinpath('latest_day.csv')

    if file.exists():
        # Read a portion of the file to get date info
        data = pd.read_csv(file, nrows=5, parse_dates=['Date'])
        latest_date = data['Date'].max()
        time_now = pd.to_datetime('now')

        if (time_now - latest_date).days > 1:
            # Since the data source is updated once a day with data for the
            # previous day, the gap in days could get to 2, but only for a
            # few hours.
            print('Fetching fresh data...')
            refresh_datasets()
    else:
        # Download fresh copies if the file is missing
        print('Downloading data...')
        refresh_datasets()
