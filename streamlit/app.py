import pandas as pd
import streamlit as st
import os
import sys; sys.path.append(os.getcwd())
from views import model_comparison, prediction

# views 
views = ['Model Comparison', 'Prediction']
view = st.sidebar.radio("Switch View", views)

if view == views[0]: 
    model_comparison.show()

if view == views[1]: 
    prediction.show()