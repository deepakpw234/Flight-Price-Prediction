from flask import Flask, redirect, render_template, request
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from src.pipelines.predict_pipeline import CustomData,PredictPipeline


application = Flask(__name__)

app = application

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home",methods=["GET","POST"])
def predict_price():
    if request.method == "GET":
        return render_template("home.html")
    else:
        data = CustomData(
            Airline=request.form.get("Airline"),
            Source=request.form.get("Source"),
            Destination=request.form.get("Destination"),
            Total_Stops=request.form.get("Total_Stops"),
            Day=request.form.get("Day"),
            Month=request.form.get("Month"),
            Year=request.form.get("Year"),
            Dep_hour=request.form.get("Dep_hour"),
            Dep_min=request.form.get("Dep_min"),
            Arrival_hour=request.form.get("Arrival_hour"),
            Arrival_min=request.form.get("Arrival_min"),
            duration_hours=request.form.get("Arrival_hour"),
            duration_minutes=request.form.get("duration_minutes"),
            duration=request.form.get("duration")
        )

        pred_df = data.get_data_as_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict_price(pred_df)

        return render_template('home.html',results=results[0])



if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)