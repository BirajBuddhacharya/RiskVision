import pandas as pd 
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle

def process_stroke(features):  
    # Encoding categorical data
    with open('models/stroke/encoder.pkl', 'rb') as fp: 
        encoder = pickle.load(fp) # loading encoder from trained data
 
    categorical_columns = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
    encoded_columns = pd.DataFrame(encoder.transform(features[categorical_columns]), 
                                   columns=encoder.get_feature_names_out(categorical_columns),
                                   index=features.index)  # Ensure indices match

    # Concatenating the original dataframe with encoded columns
    features = pd.concat([features.drop(categorical_columns, axis=1), encoded_columns], axis=1)
    
    # Normalizing numerical features
    numerical_features = ['age', 'avg_glucose_level', 'bmi']
    with open('models/stroke/scaler.pkl', 'rb') as fp: 
        scaler = pickle.load(fp)

    features[numerical_features] = scaler.transform(features[numerical_features])
    
    return features