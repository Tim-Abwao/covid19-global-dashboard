# COVID-19 Global Dashboard

## View the situation accross the globe

![global screencast](cov19_dash/assets/global-screencast.gif)

## Compare Countries

![countries screencast](cov19_dash/assets/countries-screencast.gif)

## View & get the data

![data screencast](cov19_dash/assets/data-screencast.gif)

Built with [Dash][dash]. The data is obtained from the [JHU CSSE COVID-19 Data][jhucsse] repository.

## Running locally

1. Download the code, and create a virtual environment:

    ```bash
    git clone https://github.com/Tim-Abwao/covid19-global-dashboard.git
    cd covid19-global-dashboard
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages:

    ```bash
    pip install -U pip
    pip install -r requirements.txt
    ```

3. Launch the dashboard server:

    ```bash
    waitress-serve cov19_dash:server
    ```

[dash]: https://plotly.com/dash/
[jhucsse]: https://github.com/CSSEGISandData/COVID-19
