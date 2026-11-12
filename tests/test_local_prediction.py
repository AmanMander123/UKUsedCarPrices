import math
import re
import unittest
from threading import Thread
from unittest.mock import patch

from werkzeug.serving import make_server

from api.app import app as prediction_api
from api.app import load_model
from webapp.app import app as webapp


class LocalPredictionTest(unittest.TestCase):
    def test_form_renders_a_finite_price_from_the_checked_in_model(self):
        sample = {
            "year": "2018",
            "mileage": "30000",
            "tax": "145",
            "mpg": "50",
            "engineSize": "1.5",
            "transmission": "Manual",
            "fueltype": "Petrol",
            "make": "Ford",
            "model": "Fiesta",
        }
        load_model()
        api_server = make_server("127.0.0.1", 0, prediction_api)
        thread = Thread(target=api_server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{api_server.server_port}/"
            with patch.dict(webapp.config, {"PREDICTION_API_URL": url}):
                response = webapp.test_client().post("/predict", data=sample)
        finally:
            api_server.shutdown()
            thread.join()
            api_server.server_close()

        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200, page)
        price = re.search(r"&#163;</span>\s*([^<]+)</h2>", page)
        self.assertIsNotNone(price, page)
        self.assertTrue(math.isfinite(float(price.group(1))))
