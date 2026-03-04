custom_data = {
    # Stroke dataset
    'gender': {
        'label': 'Gender',
        'description': 'Biological gender of the individual'
    },
    'age': {
        'label': 'Age (years)',
        'description': 'Age in years'
    },
    'hypertension': {
        'label': 'Hypertension',
        'description': 'History of hypertension (high blood pressure)'
    },
    'ever_married': {
        'label': 'Ever Married',
        'description': 'Marital status of the individual'
    },
    'work_type': {
        'label': 'Work Type',
        'description': 'Type of occupation'
    },
    'Residence_type': {
        'label': 'Residence Type',
        'description': 'Type of residence (urban or rural)'
    },
    'avg_glucose_level': {
        'label': 'Average Glucose Level (mg/dL)',
        'description': 'Normal: 70-99 mg/dL'
    },
    'bmi': {
        'label': ('Height (m)', 'Weight (kg)'),
        'description': ('Height (m)', 'Weight (kg)'),
        'dependents': ['height', 'weight'],
        'formula': 'weight / height**2'
    },
    'smoking_status': {
        'label': 'Smoking Status',
        'description': 'Smoking habits'
    },
    
    # Diabetes dataset
    'Pregnancies': {
        'label': 'Number of Pregnancies',
        'description': 'Count of pregnancies',
    },
    'BloodPressure': {
        'label': 'Systolic Blood Pressure (mm Hg)',
        'description': 'Normal: 120 mm Hg'
    },
    'SkinThickness': {
        'label': 'Triceps Skin Fold Thickness (mm)',
        'description': 'Normal: 10-20 mm'
    },
    'Insulin': {
        'label': 'Insulin Level (mIU/L)',
        'description': 'Normal: 16-166 mIU/L'
    },
    'DiabetesPedigreeFunction': {
        'label': ['1st° Relative With Diabetes', '2nd° Relative With Diabetes', 'Age (years)'],
        'description': ['parents, siblings', "grandparents, aunts, uncles", 'Age in years'],
        'dependents': ['firstDegreeRelative', 'SecondDegreeRelative', 'age'],
        'formula': '0.5*(firstDegreeRelative+SecondDegreeRelative) + 0.3*(1*firstDegreeRelative+2*SecondDegreeRelative) + 0.2*factor(age) + 0.1'
    },
    
    # Heart Disease dataset
    'cp': {
        'label': 'Chest Pain Type',
        'description': 'Type of chest pain experienced'
    },
    'chol': {
        'label': 'Cholesterol Level (mg/dL)',
        'description': 'Normal: <200 mg/dL'
    },
    'restecg': {
        'label': 'Resting ECG Results',
        'description': 'Electrocardiographic results at rest'
    },
    'thalach': {
        'label': 'Maximum Heart Rate (bpm)',
        'description': 'Normal: 60-100 bpm at rest'
    },
    'exang': {
        'label': 'Exercise Induced Angina',
        'description': 'Angina caused by exercise'
    },
    'oldpeak': {
        'label': 'ST Depression (mm)',
        'description': 'Normal: ~0 mm'
    },
    'slope': {
        'label': 'Slope of Peak Exercise',
        'description': 'Normal: < 1'
    },
    'ca': {
        'label': 'Vessels Colored by Fluoroscopy',
        'description': 'Number of major vessels colored by fluoroscopy'
    },
    'thal': {
        'label': 'Thalassemia Type',
        'description': 'Type of thalassemia disorder'
    },
    'fbs': {
        'label': ['Average Glucose Level'],
        'description': ['Normal: 70-100 mg/dL'],
        'dependents': ['avg_glucose_level'],
        'formula': '"Yes" if avg_glucose_level > 120 else "No"'
    }
}
