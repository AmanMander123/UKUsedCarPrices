# UK used car price estimator

A 2021 project that explored how mileage, vehicle age, and other listing attributes relate to used car prices. The web app lets someone enter a vehicle's details and see a model estimate. It uses historical data and is an engineering example, not a current valuation service.

## What I built

I used a [public UK car dataset](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes) to explore pricing patterns in the [notebook](UKUsedCarPricePrediction.ipynb). I put the fitted regression behind a Flask API and built a separate Flask web app that calls it. The original deployment used AWS Lambda.

## Design tradeoff

Separating the form from the model API lets the same prediction service support other callers and lets each side change independently. It adds an HTTP boundary, so the web app needs to handle a missing or invalid prediction. The API URL is configurable so the local walkthrough does not depend on the historical deployment.

## Run the local sample

From the repo root, with Python 3.11:

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-demo.txt
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

For a browser walkthrough, activate the same environment in two terminals. Run `python -m api.app` in one and `python -m webapp.app` in the other. Open `http://127.0.0.1:5001/` and submit this example:

| Year | Mileage | Tax | MPG | Engine size | Transmission | Fuel | Make | Model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2018 | 30000 | 145 | 50 | 1.5 | Manual | Petrol | Ford | Fiesta |

## What the check covers

The smoke test submits the example through the web app, which calls a loopback API running the checked-in model, and checks that the result page contains a finite price. It does not check current market accuracy or the original AWS deployment.

## Operating the app

The web app defaults to `http://127.0.0.1:5000/` for its API. Set `PREDICTION_API_URL` before starting the web app to use a different endpoint. The historical dependency lists are kept in the API and web app directories; use the separate demo list for local inference. Only load the trusted model artifact from this repository. The checked-in model was saved with scikit-learn 0.22.2.post1, so the demo environment emits a [version compatibility warning](https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations).

Historical references: [deployment write-up](https://amandeep-mander.medium.com/how-to-develop-a-full-stack-machine-learning-web-app-using-aws-lambda-flask-and-zappa-cf78e6454b08) and [data analysis](https://amandeep-mander.medium.com/an-analysis-on-used-car-prices-from-the-uk-6ba5c983407d). Neither is needed for the local demo.
