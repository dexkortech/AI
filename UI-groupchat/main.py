import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from phase1_message_classification.classifier import hybrid_classification
from phase1_message_classification.redis_storage import RedisStorage
import datetime
import uuid

app = Flask(__name__)
storage = RedisStorage()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user")
    text = data.get("text")
    timestamp = datetime.datetime.utcnow().isoformat()
    
    if not user or not text:
        return jsonify({"error": "User and text are required"}), 400
    
    # Classify if AI response is needed
    ai_response_needed = hybrid_classification(text)
    
    message = {
        "id": str(uuid.uuid4()),
        "user": user,
        "text": text,
        "timestamp": timestamp,
        "ai_response_needed": ai_response_needed
    }
    
    storage.store_message(message)
    return jsonify({"message": "Message stored", "ai_response_needed": ai_response_needed})

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = storage.get_messages()
    return jsonify(messages)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    ai_response_needed = hybrid_classification(text)
    return jsonify({"ai_response_needed": ai_response_needed})

@app.route('/clear', methods=['DELETE'])
def clear_messages():
    storage.clear_messages()
    return jsonify({"message": "Chat history cleared"})

if __name__ == '__main__':
    app.run(debug=True)
