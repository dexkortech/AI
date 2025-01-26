from classifier import hybrid_classification

if __name__ == "__main__":
    test_messages = [
    # Direct Questions
    "What time does the meeting start?",
    "How do I reset my password?",
    "Why is the sky blue?",
    "Can you tell me a joke?",

    # Bot Mentions
    "@bot help me with my account.",
    "@bot what is the capital of France?",
    "@chatbot, I need assistance.",
    
    # General Information & Definitions
    "Tell me the definition of artificial intelligence.",
    "Explain how blockchain works.",
    "Describe the importance of cybersecurity.",
    "Define machine learning.",
    
    # Small Talk & Casual Conversation
    "Hey, how's it going?",
    "Good morning everyone!",
    "What's up?",
    "I'm feeling great today!",
    
    # Statements (Not AI-Relevant)
    "I love pizza.",
    "That movie was amazing!",
    "It's really hot outside today.",
    "I finished my project yesterday.",
    
    # Ambiguous Cases
    "Help!",
    "I need some support.",
    "Could you assist?",
    "Not sure what to do next.",
    "Can someone help?",
    
    # Edge Cases
    "Hello?",
    "@bot",
    "Definition: AI (Artificial Intelligence)",
    "Can you explain?",
    "AI chatbot."
]


    for msg in test_messages:
        result = hybrid_classification(msg)
        print(f"Message: {msg} -> AI Response Needed: {result}")
