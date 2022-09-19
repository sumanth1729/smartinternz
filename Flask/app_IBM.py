import pickle
from flask import Flask, render_template, request
import requests

API_KEY = "uFA5uNHMQQ4kptFGA0wIgoCAaDWBYDQ4VzF4lhyFy9Fr"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/home')
def home1():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/pred', methods=['POST'])
def pred():
    department = request.form['department']
    education = request.form['education']
    if education == '1':
        education = 1
    elif education == '2':
        education = 2
    else:
        education = 3
    no_of_trainings = request.form['no_of_trainings']
    age = request.form['age']
    previous_year_rating = request.form['previous_year_rating']
    length_of_service = request.form['length_of_service']
    KPIs = request.form['KPIs']
    if KPIs == '0':
        KPIs = 0
    else:
        KPIs = 1
    awards_won = request.form['awards_won']
    if awards_won == '0':
        awards_won = 0
    else:
        awards_won = 1
    avg_training_score = request.form['avg_training_score']
    total = [[department, education, no_of_trainings, age, float(previous_year_rating), float(length_of_service),
              KPIs, awards_won, avg_training_score]]


    payload_scoring = {"input_data": [{"field": [['department', 'education', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs','awards_won','avg_training_score']],
                                       "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/28a23ca6-5cdf-4148-a60a-5ea7e3c00ff9/predictions?version=2022-01-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)

    pred = response_scoring.json()

    prediction = pred['predictions'][0]['values'][0][0]

    if prediction == 0:
        text = 'Sorry, you are not eligible for promotion'
    else:
        text = 'Great, you are eligible for promotion'
    return render_template('submit.html', predictionText=text)


if __name__ == '__main__':
    app.run(debug=True)





