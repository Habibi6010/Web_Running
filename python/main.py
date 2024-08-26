from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return jsonify({"message":"Saeed"})



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # Need to Connect to Database to check the email and password
    if email == 'test@gmail.com' and password == '123':
        return jsonify({"accsess":True})
    else:
        return jsonify({"accsess":False})

@app.route('/contact_us', methods=['POST'])
def contact_us():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    
    print(name, email, subject, message)
    # Need to Connect to Database to save the data
    return jsonify({"accsess":True})

@app.route('/run_analysis', methods=['POST'])
def run_analysis():

    video_file=request.files.get('videoUpload')
    height_runner = request.form.get('height_runner')
    selectedModel = request.form.get('selectedModel')
    settings_colors = request.form.get('settings_colors')
    settings_colors = json.loads(settings_colors) if settings_colors else {}
    print(height_runner, selectedModel, settings_colors)
    # Need to Connect to Database to save the data
    return jsonify({"response":True})

if __name__ == '__main__':
    app.run(debug=True)