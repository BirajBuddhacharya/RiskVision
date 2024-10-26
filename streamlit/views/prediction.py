import pandas as pd 
import streamlit as st
from utils.global_modules import model_selection, disease_selection, feature_selection, load_features, encode


def get_input(features): 
    # loading features config file to get info on categorical values
    features_config = load_features()
    
    # initializing empty dict to store user input
    user_input = {}
    
    # looping through each disease 
    for disease_name, disease in features.items(): 
        st.sidebar.subheader(f"features of {disease_name}")
        
        # initialize the nested dictionary for each disease
        user_input[disease_name] = {}
        
        for feature in disease: 
            # selectbox for categorical value else number_input
            options = features_config[disease_name][feature]['options']
            user_input[disease_name][feature] = st.sidebar.selectbox(feature, options) if options else st.sidebar.number_input(feature)
            
    return user_input

def predict(user_input, models):
    def predict_risk(disease_data, disease_name, model):
        features = disease_data.keys()

        # Load training dataset
        df = pd.read_csv(f"../data/processed/{disease_name}.csv")

        # Splitting data
        X = df[features]
        y = df[disease_name]

        # Encoding training data
        X, encoder, scaler = encode(X)

        # Training the model
        model.fit(X, y)

        # Transforming user input into DataFrame
        disease_df = pd.DataFrame([disease_data])

        # Ensure encoding is consistent
        disease_df, _, _ = encode(disease_df, encoder=encoder, scaler=scaler, pre_processor_flag=False)

        # Predicting risk
        risk = model.predict_proba(disease_df)[:,1]

        return risk[0] * 100  # returning percentage

    # Prediction for each disease
    for disease_name, disease_data in user_input.items():
        st.header(disease_name.upper())

        # Prediction by model
        columns = st.columns(len(models))
        for col, model in zip(columns, models):
            col.write(f"**{model.__class__.__name__}**")
            # Predicting risk
            prediction = predict_risk(disease_data, disease_name, model)

            # Displaying results
            col.write(f"**{prediction:.2f}%**") # round up to 2 decimal place
            col.write(f"Chance of having {disease_name}")
            
    
def show(): 
    st.sidebar.title("Prediction")
    
    # Getting models from user
    models = model_selection()
    
    # Disease selection
    diseases = disease_selection()
    
    # Selecting features of diseases
    features = feature_selection(diseases)
    
    # getting input from the user
    user_input = get_input(features)
    
    start = st.sidebar.button("Predict")

    if start: 
        # displaying prediction
        predict(user_input, models)
    