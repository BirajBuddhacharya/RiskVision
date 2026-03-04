import json
from config.config import features_config_loc

def load_features(): 
    # opening features config file
    print('loading features file')
    with open(features_config_loc, 'r') as fp: 
        features = json.load(fp)
    
    print("features.json loaded successfully")
    
    # returning features
    return features