# COVID-19 Global Dashboard

Track COVID-19 cases worldwide.

[![Update Datasets](https://github.com/Tim-Abwao/covid19-global-dashboard/actions/workflows/data.yml/badge.svg)](https://github.com/Tim-Abwao/covid19-global-dashboard/actions/workflows/data.yml)
[![python3.10](https://github.com/Tim-Abwao/covid19-global-dashboard/actions/workflows/test.yml/badge.svg)](https://github.com/Tim-Abwao/covid19-global-dashboard/actions/workflows/test.yml)

1. View global metrics:

    [![global screencast](screencasts/global.gif)][live_app]

2. Compare the situation among Countries:

    [![countries screencast](screencasts/countries.gif)][live_app]

Built with [Dash][dash].

The data is obtained from:

* [Our World in Data  COVID-19 data repository][owid]
* [JHU CSSE COVID-19 data repository][jhucsse]

## Running Locally

> **NOTE:** Requires **python3.10 and above**

### I. Virtual environment

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
    waitress-serve covid19_dash:server
    ```

    Afterwards, browse to <http://localhost:8080>.

### II. Docker

Fetch the image from [Docker Hub][docker-hub]:

```bash
docker pull abwao/covid19-dash:latest
docker run --rm -p 8080:8080 --name covid19-dashboard abwao/covid19-dash
```

Afterwards, browse to <http://localhost:8080>.

[dash]: https://plotly.com/dash/
[owid]: https://github.com/owid/covid-19-data/tree/master/public/data
[jhucsse]: https://github.com/CSSEGISandData/COVID-19
[live_app]: https://covid19-global-dash.herokuapp.com/
[docker-hub]: https://hub.docker.com/r/abwao/covid19-dash
