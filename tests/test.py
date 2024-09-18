import pickle
import pandas as pd 
from sklearn.linear_model import LogisticRegression

with open('tests/stroke-predict.pkl', 'rb') as fp: 
    model = pickle.load(fp)
    X_test = pd.read_csv("tests/X_test.csv")
    print(model.predict(X_test))