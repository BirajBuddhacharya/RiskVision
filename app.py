from flask import Flask, request, render_template, session, redirect
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
            
        
        # handling derived attributes 
        def factor(age):
            """ age factor: calculate factor of age based on age range"""
            if age < 25:
                return 0.0
            elif 25 <= age < 35:
                return 0.5
            elif 35 <= age < 45:
                return 1.0
            elif 45 <= age < 55:
                return 1.5
            elif 55 <= age < 65:
                return 2.0
            elif 65 <= age < 75:
                return 2.5
            else:  # 75 and older
                return 3.0

        featuers_config = load_features()
        for disease, disease_data in featuers_config.items(): 
            for feature, feature_data in disease_data.items(): 
                if feature_data.get('formula', None): 
                    for dependent in feature_data['dependents']: 
                        feature_data['formula'] = feature_data['formula'].replace(dependent, str(data.get(dependent)))

                    try: 
                        data[feature] = eval(feature_data['formula'])
                    except TypeError: # skipping if data for formula not found
                        pass
                                 
        # dataframe
        print("Making pandas dataframe of collected data")
        df = pd.DataFrame([data])
        
        # returning data frame
        return df

    # collecting data from form and turning into dataframe
    df = collect_data(request.form)
    
    # predicting stroke risk 
    try: 
        diseases_risk = predict.predict(df, session['selectedDiseases'])
    except KeyError: # handling incorrect session
        return "Error: Session vairable not accessible pls refresh the page"
    
    # Displaying result
    print("Displaying results")
    
    return render_template('predictRisk.html', diseases_risk = diseases_risk)

if __name__  == '__main__': 
    app.run(host="0.0.0.0", port=5000) 