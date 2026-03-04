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
    from config.features_metadata import custom_data
        
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