import redis
import json
import redis.exceptions
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

class RedisStorage:
    def __init__(self, host='localhost', port=None, db=0, max_messages=50):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            decode_responses=True,
            username="default",
            password=os.getenv("REDIS_PASSWORD"),
        )
        self.max_messages = max_messages
        self.redis_key = "chatbot:recent_messages"

    def store_message(self, user, message, ai_needed):
        """
        Stores a new message in Redis with structured format.
        Maintains a fixed size of max_messages by evicting the oldest message.
        """
        try:
            messages = self.get_messages()
            message_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "user": user,
                "message": message,
                "ai_needed": ai_needed
            }
            
            messages.append(message_entry)
            
            if len(messages) > self.max_messages:
                messages.pop(0)  # Remove oldest message
            
            self.redis_client.set(self.redis_key, json.dumps(messages))
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")

    def get_messages(self):
        """
        Retrieves the last max_messages from Redis.
        """
        try:
            messages_json = self.redis_client.get(self.redis_key)
            if messages_json:
                return json.loads(messages_json)
            return []
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            return []

    def clear_messages(self):
        """
        Clears all stored messages from Redis.
        """
        try:
            self.redis_client.delete(self.redis_key)
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")

# Example usage
if __name__ == "__main__":
    storage = RedisStorage()
    storage.store_message("JohnDoe", "Hello, how are you?", False)
    print("Stored messages:", storage.get_messages())
    # get message
    messages = storage.get_messages()
    print(messages)
