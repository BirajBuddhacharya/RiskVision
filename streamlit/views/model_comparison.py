import pandas as pd 
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from utils.global_modules import model_selection, disease_selection, feature_selection, encode
        
def model_evaluate(models, diseases, features): 
    def train_evaluate(model, X, y):  
        # Splitting into testing and training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        
        # Training model 
        model.fit(X_train, y_train)
        
        # Predicting
        y_pred = model.predict(X_test)
        
        metrics = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred),
            'F1-Score': f1_score(y_test, y_pred),
        }
        
        return metrics
        
    for disease in diseases: 
        # Section header for each disease
        st.title(disease.upper())
        
        # Loading and encoding data for each model 
        try: 
            df = pd.read_csv(f"../data/processed/{disease}.csv")  
        except FileNotFoundError: 
            st.write(f"Error loading dataset for {disease}")
            return 
        
        # Correcting feature selection access
        X = encode(df[features[disease]])[0] # returns tuple of transformed data encoder and scaler
        y = df[disease]
        
        # Creating columns for each model
        columns = st.columns(len(models))
        
        # Evaluating each model
        for col, model in zip(columns, models): 
            col.write(f"**{model.__class__.__name__}**")  # Displaying model name
            metrics = train_evaluate(model, X, y)
            
            for key, value in metrics.items():  # Use items() to iterate key-value pairs
                col.write(f"**{key}**: {value}")  # Use Markdown for better formatting
    
def show(): 
    st.sidebar.header("Model Comparison")
    
    # Getting models from user
    models = model_selection()
    
    # Disease selection
    diseases = disease_selection()
    
    # Selecting features of diseases
    features = feature_selection(diseases)
    
    # Evaluate model 
    evaluate = st.sidebar.button("Evaluate")
    
    if evaluate: 
        model_evaluate(models, diseases, features)
