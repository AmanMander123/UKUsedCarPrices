import os
from math import isfinite

import requests
from flask import Flask, abort, render_template, request

app = Flask(__name__)
app.config["PREDICTION_API_URL"] = os.environ.get(
    "PREDICTION_API_URL", "http://127.0.0.1:5000/"
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def predict():
    fields = ("year", "mileage", "tax", "mpg", "transmission", "fueltype", "make", "model")
    params = {field: request.form[field].strip() for field in fields}
    params["enginesize"] = request.form["engineSize"].strip()

    try:
        response = requests.get(app.config["PREDICTION_API_URL"], params=params, timeout=5)
        response.raise_for_status()
        prediction = float(response.json()["result"])
    except (requests.RequestException, KeyError, TypeError, ValueError):
        abort(502, description="The prediction API did not return a price.")
    if not isfinite(prediction):
        abort(502, description="The prediction API did not return a finite price.")

    return render_template("result.html", prediction=prediction)


if __name__ == "__main__":
    app.run(port=5001)
