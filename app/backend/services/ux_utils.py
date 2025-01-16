""" # app.py
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import json_util
import json
import os

app = Flask(__name__)
# Configure CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],  # Add your frontend URL
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/solvi")
mongo = PyMongo(app)

# Base API URL
API_BASE_URL = '/api/solvi/v1'

@app.route(API_BASE_URL, methods=['POST'])
def create_project():
    try:
        project_data = request.json
        # Add any additional fields like timestamp, user_id, etc.
        result = mongo.db.projects.insert_one(project_data)
        
        return jsonify({
            "success": True,
            "message": "Project created successfully",
            "project_id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route(API_BASE_URL, methods=['GET'])
def get_projects():
    try:
        projects = list(mongo.db.projects.find())
        # Convert ObjectId to string for JSON serialization
        return json.loads(json_util.dumps(projects)), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) """