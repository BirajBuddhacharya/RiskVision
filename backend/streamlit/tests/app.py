import streamlit as st

# Sidebar - Simulating a Navbar
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio('Go to', ['Home', 'Model Comparison', 'About'])

# Home Page
if nav_option == 'Home':
    st.title("Welcome to the Model Comparison App")
    st.write("""
    This app allows you to compare different machine learning models on accuracy.
    Use the sidebar to navigate through the app.
    """)

# Model Comparison Page
elif nav_option == 'Model Comparison':
    st.title("Model Comparison")

    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score

    # Load the dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Model Selection
    st.sidebar.subheader('Choose a model')
    model_choice = st.sidebar.selectbox(
        'Select model',
        ('Logistic Regression', 'Decision Tree', 'Random Forest')
    )

    # Define models
    models = {
        'Logistic Regression': LogisticRegression(),
        'Decision Tree': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier()
    }

    # Train and evaluate the selected model
    model = models[model_choice]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Display results
    st.write(f"The accuracy of the {model_choice} model is **{accuracy:.2f}")
