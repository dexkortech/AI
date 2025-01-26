import redis
import json
import redis.exceptions

class RedisStorage:
    def __init__(self, host='localhost', port=6379, db=0, max_messages=50):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.max_messages = max_messages
        self.redis_key = "chatbot:recent_messages"

    def store_message(self, message):
        """
        Stores a new message in Redis.
        Maintains a fixed size of max_messages by evicting the oldest message.
        """
        try:
            messages = self.get_messages()
            messages.append(message)
            
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
    storage.store_message({"text": "Hello, bot!", "ai_needed": True})
    print("Stored messages:", storage.get_messages())
