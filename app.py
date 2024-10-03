from flask import Flask, request, render_template, session
import pandas as pd
from utils import predict
from utils.modules import load_features
import os 

# Initializing Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# formating strings for frontend
@app.template_filter('format_str')
def format_str(string): 
    return string.replace('_', ' ').title()

@app.route('/')
def diseasesInput():
    diseases_config = load_features() 
    diseases = list(diseases_config.keys())
    return render_template('diseasesInput.html', diseases = diseases)

@app.route('/questionere', methods = ['POST'])
def questionere(): 
    def load_and_group(): 
        # finding common questions
        diseases = load_features() # loading feature files

        # selecting only user selected disease
        selectedDiseases = request.form.getlist('selectedDiseases[]')
        diseases = {key: value for key, value in diseases.items() if key in selectedDiseases}
        
        # storing user selected diseases in session to use in predict page
        session['selectedDiseases'] = selectedDiseases
        
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
        
        # returning grouped data and user selected diseases
        return question_group, selectedDiseases
    
    # loading features and grouping them on the basic of common and disease
    question_group, selectedDiseases = load_and_group()
    
    return render_template('index.html', question_group = question_group, selectedDiseases = selectedDiseases)

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
    diseases_risk = predict.predict(df, session['selectedDiseases'])
    
    # Displaying result
    print("Displaying results")
    
    return render_template('predictRisk.html', diseases_risk = diseases_risk)


if __name__  == '__main__': 
    app.run(debug=True)