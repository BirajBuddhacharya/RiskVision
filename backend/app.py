from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from utils import predict
from utils.modules import load_features
import os 

# Initializing Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

@app.route('/api/diseases', methods=['GET'])
def diseasesInput():
    diseases_config = load_features() 
    diseases = list(diseases_config.keys())
    return jsonify({"diseases": diseases})

@app.route('/api/questionere', methods=['POST'])
def questionere(): 
    def load_and_group(): 
        # finding common questions
        diseases = load_features() # loading feature files

        # selecting only user selected disease
        data = request.get_json()
        if not data:
            data = {}
        selectedDiseases = data.get('selectedDiseases', [])
        diseases = {key: value for key, value in diseases.items() if key in selectedDiseases}
        
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
    
    try:
        # loading features and grouping them on the basic of common and disease
        question_group, selectedDiseases = load_and_group()
        return jsonify({"question_group": question_group, "selectedDiseases": selectedDiseases})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/predictRisk', methods=['POST'])
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
    data_payload = request.get_json()
    if not data_payload:
        data_payload = {}
    form_data = data_payload.get('form_data', {})
    selectedDiseases = data_payload.get('selectedDiseases', [])

    df = collect_data(form_data)
    
    # predicting stroke risk 
    try: 
        diseases_risk = predict.predict(df, selectedDiseases)
    except Exception as e: # handling incorrect inputs or prediction failure
        return jsonify({"error": str(e)}), 400
    
    # Displaying result
    print("Displaying results")
    
    import numpy as np
    def make_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [make_serializable(i) for i in obj]
        return obj

    serializable_risk = make_serializable(diseases_risk)
    
    return jsonify({"diseases_risk": serializable_risk})

if __name__  == '__main__': 
    app.run(host="0.0.0.0", port=5000) 