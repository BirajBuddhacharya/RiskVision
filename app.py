from flask import Flask, request, render_template
import pandas as pd
import pickle
from utils import predict

# Initializing Flask app
app = Flask(__name__)

def collect_data(info): 
    print("collecting data")
    
    # turning the info into dict to change into dataframe
    data = dict(info)
    
    # defining dereived units
    data['bmi'] = [float(info.get('weight', 0.0)) / float(info.get('height', 1.0))**2]
    
    # dataframe
    print("Making pandas dataframe of collected data")
    df = pd.DataFrame(data)
    
    # returning data frame
    return df

@app.route('/')
def index(): 
    return render_template('index.html')


@app.route('/predictRisk', methods=['POST'])
def predictRisk():
    try:
        # collecting data from form and turning into dataframe
        df = collect_data(request.form)

        # predicting stroke risk 
        stroke_risk = predict.predictStroke(df)

        # Displaying result
        print("Displaying results")
        return render_template('predictRisk.html', stroke_risk=stroke_risk[0])

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