from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

car = pd.read_csv("Project3_car_price_predictor/data/cleaned_car.csv")

@app.route("/")
def index():
    
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_types = sorted(car['fuel_type'].unique())
    
    return render_template("index.html", companies=companies, car_models=car_models, years=years, fuel_types=fuel_types)

@app.route("/predict", methods=['POST'])
def predict():
    company = request.form.get("company")
    car_model = request.form.get("model")
    year = int(request.form.get("year"))
    fuel_type = request.form.get("fuel_type")
    kms_driven = int(request.form.get("kms_driven"))
    
    print(company, car_model, year, fuel_type, kms_driven)
    
    model = pickle.load(open("Project3_car_price_predictor/LinearRegressionModel.pkl", "rb"))
    
    prediction = model.predict(
        pd.DataFrame(
            [
                [car_model, company, year, kms_driven, fuel_type]
            ],
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
        )
    )
    
    return str(np.round(prediction[0], 2)) # it's a list, numpy to round the data to 2 digits place, and converting it to string.
    
if __name__=="__main__":
    app.run(debug=True)