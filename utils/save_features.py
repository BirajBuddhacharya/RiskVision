import json

def save_features(save_feature: dict):  # expecting save_feature to have only one key-value pair
    try:
        # Attempt to open and load the JSON file, initialize empty if not found
        try:
            with open('config/features.json', 'r') as fp:
                features = json.load(fp)
        except FileNotFoundError:
            print("Warning: features.json not found, initializing empty features.")
            features = {}

        # Ensure only one key-value pair is passed
        save_feature_key = list(save_feature.keys())

        if len(save_feature_key) != 1:
            print("Error: save_feature expects exactly one key, value pair.")
            return  # Return instead of exiting to prevent abrupt termination

        # Extract the single key-value pair
        save_feature_key = save_feature_key[0]  # Convert to str from list

        # Add the feature to the existing features
        features[save_feature_key] = save_feature[save_feature_key]

        # Save the updated features back to the JSON file
        with open('config/features.json', 'w') as fp:
            json.dump(features, fp)
        print(f"Successfully saved feature: {save_feature_key}")

    except json.JSONDecodeError as e:
        print("Error: Could not decode JSON.")
        print(e)
    except Exception as e:
        print("An unexpected error occurred: ")
        print(e)
