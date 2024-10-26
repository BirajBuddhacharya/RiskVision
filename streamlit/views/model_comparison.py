import pandas as pd 
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from utils.global_modules import model_selection, disease_selection, feature_selection, encode
import matplotlib.pyplot as plt
        
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
        
        store_df = {} # dict to store metrics of each model 
        # Evaluating each model
        for model in models: 
            store_df[model.__class__.__name__] = train_evaluate(model, X, y)

        # Making dataframe of collected data
        metrics_df = pd.DataFrame(store_df).T
        
        # Apply dark mode style
        plt.style.use('dark_background')
        
        # Plotting the bar graph
        metrics_df.plot(kind='bar', figsize=(8, 5), color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        plt.title('Model Performance Comparison', color='white')
        plt.xlabel('Model', color='white')
        plt.ylabel('Scores', color='white')
        plt.xticks(rotation=0, color='white')
        plt.yticks(color='white')
        plt.legend(title='Metrics', facecolor='black', edgecolor='white', labelcolor='white')
        plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
        
        # Displaying into streamlit
        st.pyplot(plt)
    
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
