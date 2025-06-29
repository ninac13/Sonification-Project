# instance for the flask app 
from flask import Flask, render_template, redirect, url_for 
app = Flask(__name__)

# This route handles the homepage ('/')
@app.route('/')
def index():
    # Render the 'index.html' template when someone visits the homepage
    return render_template('index.html')

# sonficiation group button click 
@app.route('/sonfication')
def sonification (): 
    # message that they see once they clcik on the button for sonfiication 
    return "<h1> Welcome to the Sonficiation Group! </h1>"

# visual group button click 
@app.route('/visual')
def visual (): 
    # message that they see once they clcik on the button for visual 
    return "<h1> Welcome to the Visual Group! </h1>"

#runs the app
if __name__ == '__main__':
    # Debug mode 
    app.run(debug=True)