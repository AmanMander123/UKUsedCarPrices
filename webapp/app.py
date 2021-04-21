from flask import Flask,render_template,url_for,request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        year = request.form['year']
        mileage = request.form['mileage']
        tax = request.form['tax']
        mpg = request.form['mpg']
        engineSize = request.form['engineSize']
        transmission = request.form['transmission']
        fueltype = request.form['fueltype']
        make = request.form['make']
        model = request.form['model']

        api_url = 'https://au6ab6wlg6.execute-api.us-east-1.amazonaws.com/dev?' + 'year=' + year + '&mileage=' + mileage +'&tax=' + tax +'&mpg=' + mpg +'&enginesize=' + engineSize +'&transmission=' + transmission +'&fueltype=' + fueltype +'&make=' + make +'&model=' + model
        print(api_url)
        # Make prediction
        my_prediction_json = requests.get(api_url)
        my_prediction = my_prediction_json.json()

        return render_template('result.html', prediction=float(my_prediction['result']))

if __name__ == '__main__':
    app.run(debug=True)