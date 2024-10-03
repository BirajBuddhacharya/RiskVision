import json
import os
from config.config import features_config_loc

def save_features(feature_df, target): 
    custom_labels = {
    # Stroke dataset
    'gender': 'Gender',
    'age': 'Age',
    'hypertension': 'Hypertension',
    'heart_disease': 'Heart Disease',
    'ever_married': 'Ever Married',
    'work_type': 'Work Type',
    'Residence_type': 'Residence Type',
    'avg_glucose_level': 'Average Glucose Level',
    'bmi': 'BMI',
    'smoking_status': 'Smoking Status',
    
    # Diabetes dataset
    'Pregnancies': 'Number of Pregnancies',
    'BloodPressure': 'Blood Pressure',
    'SkinThickness': 'Skin Thickness',
    'Insulin': 'Insulin Level',
    'DiabetesPedigreeFunction': 'Diabetes Pedigree Function',
    
    # Heart Disease dataset
    'cp': 'Chest Pain Type',
    'chol': 'Cholesterol Level',
    'restecg': 'Resting ECG Results',
    'thalach': 'Maximum Heart Rate',
    'exang': 'Exercise Induced Angina',
    'oldpeak': 'ST Depression',
    'slope': 'Slope of Peak Exercise',
    'ca': 'Number of Major Vessels',
    'thal': 'Thalassemia Type'
    }
    
    # empty dict to process columns and fill in option and label for each feature
    local_features_dict = {}
    
    # assigning labels and optins for each features
    print("Starting to process columns in feature_df...")
    for column in feature_df.columns:
        try:
            # Try to use the custom label
            local_features_dict[column] = {
                'label': custom_labels[column],  # May raise KeyError
                'options': list(feature_df[column].unique()) if feature_df[column].dtype == 'object' else None
            }
        except KeyError:
            # Fallback: assign the column name as the label if custom_labels[column] does not exist
            local_features_dict[column] = {
                'label': column,  # Use column as label
                'options': list(feature_df[column].unique()) if feature_df[column].dtype == 'object' else None
            }
            # Continue to the next column
            continue


    # reading feature config file to store update data
    features_config = features_config_loc
    
    # handling no file found
    if not os.path.exists(features_config):
        print('features config file doesnt exist creating new')   
        try: 
            with open(features_config, 'w') as fp: 
                json.dump({}, fp, indent = 4)
        except FileNotFoundError: 
            print("Parent dict of featuers config file doesnt exist")
        
        
    try:
        with open(features_config, 'r') as fp: 
            global_features = json.load(fp)
   
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON (json file may not be in correct format)")
        return
    
    except Exception as e: 
        print("Unexpected error occured", e)
        
    # writing update data in featues config file
    global_features[target] = local_features_dict

    with open(features_config, 'w') as fp:
        print("Updating features config file")
        json.dump(global_features, fp, indent = 4) 
    
    print('Succesfully updated features config file')
