import os

import pandas as pd

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from nixtlats import TimeGPT

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name = name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

@app.route('/calc', methods=['POST'])
def calc():
    if request.data.decode():
        request_json = request.get_json()
        if "data" in request_json:
            data = request_json["data"]
            print('Request for calc page received with data=%s' % data)
            response_json = {"data":str(data)+" modified"}
            return response_json
        else:
            print('Request for calc page received with no name or blank name -- redirecting')
            response_json = {"data":"data was empty"}
            return response_json
    else:
        response_json = {"data":"request again without data"}
        return response_json


@app.route('/forecast', methods=['POST'])
def forecast():
    if request.data.decode():
        request_json = request.get_json()
        if "data" in request_json:
            # Get data and transform to dataframe
            df = pd.DataFrame(request_json.data)

            # Init TimeGPT API access
            timegpt = TimeGPT(
                # defaults to os.environ.get("TIMEGPT_TOKEN")
                token='my_token_provided_by_nixtla'
            )

            # Forecast with TimeGPT
            fcst_df = timegpt.forecast(df, h=24, level=[80, 90])

            # Retrieve data from response
            data = request_json["data"]
            print('Request for calc page received with data=%s' % data)

            # Prepare data for response
            response_json = {"forecast":str(data)+" forecast"}
            return response_json
        else:
            print('Request for calc page received with no name or blank name -- redirecting')
            response_json = {"data":"data was empty"}
            return response_json
    else:
        response_json = {"data":"request again without data"}
        return response_json


if __name__ == '__main__':
    print("Still running...")
    app.run()
