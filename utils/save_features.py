import json
import os
from config.config import features_config_loc
from app import format_str

def save_features(feature_df, target): 
    """
        Executed in features_selection.ipynb and saves information of each attributes of disease in features.json file
        args: 
            feature_df: dataframe of disease data
            target: name of disease
        returns: None
    """
    def custom_data(): 
        """ 
            Custom data to be set for front end
            args: None
            return: nested dict of custom_data with attributes as label 
        """
        custom_data = {
            # Stroke dataset
            'gender': {
                'label': 'Gender',
                'description': 'Biological gender of the individual'
            },
            'age': {
                'label': 'Age',
                'description': 'Age in years'
            },
            'hypertension': {
                'label': 'Hypertension',
                'description': 'History of hypertension (high blood pressure)'
            },
            'heart_disease': {
                'label': 'Heart Disease',
                'description': 'Presence of heart disease'
            },
            'ever_married': {
                'label': 'Ever Married',
                'description': 'Marital status of the individual'
            },
            'work_type': {
                'label': 'Work Type',
                'description': 'Type of occupation'
            },
            'Residence_type': {
                'label': 'Residence Type',
                'description': 'Type of residence (urban or rural)'
            },
            'avg_glucose_level': {
                'label': 'Average Glucose Level',
                'description': 'Normal: 70-99 mg/dL'
            },
            'bmi': {
                'label': ('Height', 'Weight'),
                'description': ('Height', 'Weight'),
                'dependents': ['height', 'weight'],
                'formula': 'weight / height**2'
            },
            'smoking_status': {
                'label': 'Smoking Status',
                'description': 'Smoking habits'
            },
            
            # Diabetes dataset
            'Pregnancies': {
                'label': 'Number of Pregnancies',
                'description': 'Count of pregnancies'
            },
            'BloodPressure': {
                'label': 'Systolic Blood Pressure',
                'description': 'Normal: 120 mm Hg'
            },
            'SkinThickness': {
                'label': 'Triceps skin fold Thickness',
                'description': 'Normal: 10-20 mm'
            },
            'Insulin': {
                'label': 'Insulin Level',
                'description': 'Normal: 16-166 mIU/L'
            },
            'DiabetesPedigreeFunction': {
                'label': 'Diabetes Pedigree Function',
                'description': 'Family history influence factor'
            },
            
            # Heart Disease dataset
            'cp': {
                'label': 'Chest Pain Type',
                'description': 'Type of chest pain experienced'
            },
            'chol': {
                'label': 'Cholesterol Level',
                'description': 'Normal: <200 mg/dL'
            },
            'restecg': {
                'label': 'Resting ECG Results',
                'description': 'Electrocardiographic results at rest'
            },
            'thalach': {
                'label': 'Maximum Heart Rate',
                'description': 'Normal: 60-100 bpm at rest'
            },
            'exang': {
                'label': 'Exercise Induced Angina',
                'description': 'Angina caused by exercise'
            },
            'oldpeak': {
                'label': 'ST Depression',
                'description': 'Normal: ~0 mm'
            },
            'slope': {
                'label': 'Slope of Peak Exercise',
                'description': 'Normal: < 1'
            },
            'ca': {
                'label': 'Vessels colored by fluoroscopy',
                'description': 'Number of major vessels colored by fluoroscopy'
            },
            'thal': {
                'label': 'Thalassemia Type',
                'description': 'Type of thalassemia disorder'
            },
            'fbs': {
                'label': ('Fasting Blood Sugar > 120mg'),
                'description': ['Normal: 70-100 mg/dl'],
                'dependents': ['avg_glucose_level'],
                'formula': '"Yes" if avg_glucose_level > 120 else "No"'
            }
        }
        return custom_data
    
    def save_features_config(features_config, local_features_dict):
        """
            saves the data in features.json file by the key {target}
            
            args: 
                features_config_loc: File path of features.json file (contains info of attributes of disease)
                local_features_dict: info of attributes
            
            returns: None
        """
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
        
        return
        
    # retriving custom data of attributes 
    custom_data = custom_data()    
        
    # empty dict to process columns and fill in option and label for each feature
    local_features_dict = {}
    
    # assigning labels and optins for each features
    print("Starting to process columns in feature_df...")
    for column in feature_df.columns:
        # Try to use the custom label
        local_features_dict[column] = {
            'label': custom_data.get(column, {}).get('label', format_str(column)),  
            'options': list(feature_df[column].unique()) if feature_df[column].dtype == 'object' else None,
            'desc': custom_data.get(column, {}).get('description', None),
        }
        
    # Handling derived attributes 
    for column in feature_df.columns:
        dependents = custom_data.get(column, {}).get('dependents', [])

        for index, dependent in enumerate(dependents):
            # Retrieve 'label' and 'desc' with safety checks
            labels = custom_data.get(column, {}).get('label')
            descriptions = custom_data.get(column, {}).get('description')

            local_features_dict[dependent] = {
                'label': labels[index] if labels and index < len(labels) else format_str(dependent),
                'desc': descriptions[index] if descriptions and index < len(descriptions) else None,
                'dependent': column
            }
            
        local_features_dict[column]['formula'] = custom_data.get(column, {}).get('formula', None)
        local_features_dict[column]['dependents'] = custom_data.get(column, {}).get('dependents', None)
        
        

    # saving into features.json
    save_features_config(features_config_loc, local_features_dict)