from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return jsonify({"message":"Saeed"})

@app.route('/get_data', methods=['POST'])
def get_data():
    
    data = request.json
    name = data.get('name', 'Unknown')
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == '__main__':
    app.run(debug=True)