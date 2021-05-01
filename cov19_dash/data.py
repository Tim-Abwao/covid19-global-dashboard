import pandas as pd
from pathlib import Path


BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'\
    'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19'


def fetch_data(category='confirmed'):
    """Get global covid19 data for the given category from the JHU CSSE
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

    Returns
    -------
    A pandas DataFrame with covid-19 case information.
    """
    case_data = [fetch_data(category) for category in {
                         'confirmed', 'deaths', 'recovered'}]
    case_data_df = (
        # Combine the case data into a DataFrame
        pd.concat(case_data, axis=1)
        # Restore 'Country/Region' and 'Date' as columns and set a default
        # index
        .reset_index()
    )

    case_data_df['Date'] = pd.to_datetime(case_data_df['Date'])
    return case_data_df


def refresh_datasets():
    """Save fresh copies of the data used in the dashboard.
    """
    case_data = get_case_information()

    # Save daily values
    daily_values_file = Path('data/daily_values.csv')
    case_data.to_csv(daily_values_file, index=False)
    # Save daily cummulative totals
    cummulative_totals_file = Path('data/cummulative_totals.csv')
    (case_data.groupby('Date')
     .sum()  # Get totals for each day
     .to_csv(cummulative_totals_file))


if __name__ == "__main__":
    refresh_datasets()
