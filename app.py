from flask import Flask 
from flask import request
from flask import render_template
import pandas as pd
from utils.process_features import process
import pickle

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/predictRisk', methods=['POST'])
def predictRisk():
    try:
        # Collecting data for risk prediction
        print("Collecting data")
        gender = request.form.get('gender')
        age = int(request.form.get('age', 0))
        hypertension = int(request.form.get('hypertension', 0))
        heart_disease = int(request.form.get('heart_disease', 0))
        ever_married = request.form.get('ever_married')
        work_type = request.form.get('work_type')
        Residence_type = request.form.get('Residence_type')
        avg_glucose_level = float(request.form.get('avg_glucose_level', 0.0))
        weight = float(request.form.get('weight', 0.0))
        height = float(request.form.get('height', 1.0))  # Default to 1.0 to avoid division by zero
        smoking_status = request.form.get('smoking_status')

        # Calculate BMI
        bmi = weight / height**2 if height != 0 else 0

        # Creating a dictionary with the data
        data = {
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'avg_glucose_level': [avg_glucose_level],
            'bmi': [bmi],
            'gender': [gender],
            'ever_married': [ever_married],
            'work_type': [work_type],
            'Residence_type': [Residence_type],
            'smoking_status': [smoking_status]
        }

        # Creating a Pandas DataFrame
        features = pd.DataFrame(data)

        # Processing data using OneHotEncoder and StandardScaler
        print("Processing data using OneHotEncoder and StandardScaler")
        features = process(features)

        # Load the model
        with open('models/stroke-predict.pkl', 'rb') as fp:
            model = pickle.load(fp)

        # Predicting stroke risk
        print("Predicting stroke risk")
        result = model.predict_proba(features)[:,1] * 100 # turning to percentage

        # Displaying result
        print("Displaying results")
        return render_template('predictRisk.html', result=result[0])

    except KeyError as e:
        print(f"KeyError: Missing form field - {e}")
        return "Error: Missing form field", 400

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return "Error: Model not found", 500

    except pickle.UnpicklingError as e:
        print(f"Pickle Error: {e}")
        return "Error: Unable to load the model", 500

    except Exception as e:
        print(f"Exception: {e}")
        return "An unexpected error occurred", 500

if __name__  == '__main__': 
    app.run(debug=True)