import matplotlib.pyplot as plt
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
    
    st.title('Model Prediction')
    
    # Empty to dict to store prediction 
    store_predict = {}
    
    # Prediction for each disease
    for disease_name, disease_data in user_input.items():
        store_predict[disease_name] = {}

        # Prediction by model
        for model in models:
            # Predicting risk
            prediction = predict_risk(disease_data, disease_name, model)

            store_predict[disease_name][model.__class__.__name__] = prediction
            
    # making df of stored prediction 
    predict_df = pd.DataFrame(store_predict)
    
    # Apply dark mode style
    plt.style.use('dark_background')
    
    # Plotting the bar graph
    predict_df.plot(kind='bar', figsize=(8, 5), color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Model Prediction', color='white')
    plt.xlabel('Model', color='white')
    plt.ylabel('Prediction', color='white')
    plt.xticks(rotation=0, color='white')
    plt.yticks(color='white')
    plt.legend(title='Metrics', facecolor='black', edgecolor='white', labelcolor='white')
    plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
    
    # Displaying into streamlit
    st.pyplot(plt)
    
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
    