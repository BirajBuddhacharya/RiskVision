from flask import Flask, request, render_template
import pandas as pd
from utils import predict
import json 
from config.config import features_config_loc

# Initializing Flask app
app = Flask(__name__)

# formating strings for frontend
@app.template_filter('format_str')
def format_str(string): 
    return string.replace('_', ' ').title()

@app.route('/')
def index():
    def load_and_group(features_config_loc): 
        # finding common questions
        try:
            with open(features_config_loc, 'r') as fp: 
                diseases = json.load(fp)
                print("features config file opened sucessfully")

        except FileNotFoundError: 
            print("Error finding diseases config file")
            exit

        # initializing empty list to track duplicate features 
        features = []
        
        # initializing empty dict to collect grouped data
        question_group = {'common': {}}
        
        # processing common features
        for disease_key, disease in diseases.items(): 
            for feature_key, feature in disease.items(): 
                if feature_key not in features: 
                    features.append(feature_key)
                else: 
                    question_group['common'].update({feature_key: feature})
        
        # processing disease only (disease - common)
        for disease_key, disease in diseases.items(): 
            question_group[disease_key] = {
                feature_key: feature 
                for feature_key, feature in disease.items() 
                if feature_key not in question_group['common']
            }
        
        # returning grouped data
        return question_group
    
    # loading features and grouping them on the basic of common and disease
    question_group = load_and_group(features_config_loc)

    return render_template('index.html', question_group = question_group)


@app.route('/predictRisk', methods=['POST'])
def predictRisk():
    def collect_data(info): 
        print("collecting data")

        # turning the info into dict to change into dataframe
        data = dict(info)

        # formating number convertable data
        for key, value in data.items(): 
            try: # try to convert to int
                data[key] = int(value)
            except ValueError: # try to convert to float if failed
                try: 
                    data[key] = float(value)
                except ValueError: # leaving as str if both int and float failed
                    data[key] = value
                
        # dataframe
        print("Making pandas dataframe of collected data")
        df = pd.DataFrame([data])

        # returning data frame
        return df

    # collecting data from form and turning into dataframe
    df = collect_data(request.form)
    
    # predicting stroke risk 
    diseases_risk = predict.predict(df)
    
    # Displaying result
    print("Displaying results")
    
    return render_template('predictRisk.html', diseases_risk = diseases_risk)


if __name__  == '__main__': 
    app.run(debug=True)