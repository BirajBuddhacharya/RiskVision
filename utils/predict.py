import pandas as pd 
import utils.process_features as pf
import pickle
from config import config
import json

def load_features(): 
    # opening features config file
    print('loading features file')
    with open("config/features.json", 'r') as fp: 
        features = json.load(fp)
    
    print("features.json loaded successfully")
    
    # returning features
    return features
    
def predictStroke(df): 
    try: 
        features = load_features()
        
        # selecting features 
        stroke_df = df[features['stroke_features']]
        
        # Processing data using OneHotEncoder and StandardScaler
        print("Processing data using OneHotEncoder and StandardScaler")
        stroke_df = pf.process_stroke(stroke_df)

        # Loading the model
        with open('models/stroke/stroke.pkl', 'rb') as fp:
            model = pickle.load(fp)

        # Predicting stroke risk
        print("Predicting stroke risk")
        result = model.predict_proba(stroke_df)[:,1] * 100 # turning to percentage

        return result
    
    except KeyError: 
        # finding missing colomns
        set1 = set(features['stroke_features'])
        set2 = set(df.columns)
        
        missing_columns = set1 - set2
        
        # printing findings
        print(f"following stroke features are missing: {missing_columns}")
    
    except Exception as e: 
        print("Exception occured:")
        print(e)