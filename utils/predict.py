import pandas as pd 
import pickle
from config.config import features_config_loc
import pandas as pd 
import pickle
from utils.modules import load_features

def process(features, disease):  
    # Checking if the disease exists in the features config file 
    diseases = load_features()
    
    if disease not in diseases: 
        print(f"{disease} doesn't exist in features config file")
        return None  # Return None or raise an exception
 
    # Encoding categorical data
    print(f"Encoding {disease} data")
    categorical_columns = features.select_dtypes(include='object').columns
    if not categorical_columns.empty: 
        try: 
            with open(f'models/{disease}/encoder.pkl', 'rb') as fp: 
                encoder = pickle.load(fp)  # Loading encoder from trained data
        except FileNotFoundError: 
            print("Error opening encoder")
            return None  # Return None or raise an exception
        
        encoded_columns = pd.DataFrame(
            encoder.transform(features[categorical_columns]), 
            columns=encoder.get_feature_names_out(categorical_columns),
            index=features.index  # Ensure indices match
        )

        # Concatenating the original dataframe with encoded columns
        features = pd.concat([features.drop(categorical_columns, axis=1), encoded_columns], axis=1)

    # Normalizing numerical features
    print(f"scaling {disease} data")
    numerical_features = features.select_dtypes(include='number').columns

    if not numerical_features.empty:
        try: 
            with open(f'models/{disease}/scaler.pkl', 'rb') as fp: 
                scaler = pickle.load(fp)
        except FileNotFoundError: 
            print("Error opening scaler")
            return None  # Return None or raise an exception
            
        features[numerical_features] = scaler.transform(features[numerical_features])
    
    print(f"{disease} data processed successfully ")
    return features
    
def predict(df, selectedDiseases): 
    try: 
        # loading diseases features config file
        diseases = load_features()
        
        # Debugging
        print("Selected Diseases in predict: ", selectedDiseases)
        
        # selecting only user selected disease
        diseases = {key: value for key, value in diseases.items() if key in selectedDiseases}
        
        # initializing empty distionary to store probability of diseases
        result = {}
        
        # predicting each disease in features config file
        for disease_name, disease in diseases.items(): 
            # processing data using standard scaler and OneHotEncoder
            print(f"processing data for {disease_name}")
            processed_disease = process(df[disease.keys()], disease_name)
            
            # predicting
            with open(f'models/{disease_name}/{disease_name}.pkl', 'rb') as fp: 
                model = pickle.load(fp)
            prediction = model.predict_proba(processed_disease)[:,1] * 100 # turning to percentag

            # collecting prediction 
            result[disease_name] = prediction
            
        return result

    except FileNotFoundError: 
        print(f"Error opening {disease_name} model")
        exit(1)
    
    except Exception as e: 
        print("Exception occured:")
        print(e)