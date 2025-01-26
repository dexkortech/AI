from flask import Flask, request, jsonify
from phase_1_message_classification.redis_storage import RedisStorage
from phase_1_message_classification.classify_message import classify_message

import datetime
import uuid

app = Flask(__name__)
storage = RedisStorage()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user")
    text = data.get("text")
    timestamp = datetime.datetime.utcnow().isoformat()
    
    if not user or not text:
        return jsonify({"error": "User and text are required"}), 400
    
    # Classify if AI response is needed
    ai_response_needed = classify_message(text)
    
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
    
    ai_response_needed = classify_message(text)
    return jsonify({"ai_response_needed": ai_response_needed})

@app.route('/clear', methods=['DELETE'])
def clear_messages():
    storage.clear_messages()
    return jsonify({"message": "Chat history cleared"})

if __name__ == '__main__':
    app.run(debug=True)
