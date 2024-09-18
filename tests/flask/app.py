from flask import Flask 
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('test.html')

@app.route('/submit', methods = ['POST'])
def submit(): 
    name = request.form['name']
    return f"hello {name}"

if __name__ == '__main__': 
    app.run(debug = True)