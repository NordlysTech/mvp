from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["conversation_db"]  # Create database if it doesn't exist
collection_name = "conversations"

# Ensure collection exists (MongoDB creates it on the first insertion)
def get_or_create_collection(db, collection_name):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    return db[collection_name]

# Get or create the 'history' collection
collection = get_or_create_collection(db, 'history')

def handle_user_message(user_id, conversation_id, user_message, assistant_answer):
    """
    Updates the conversation history in MongoDB with the user's message and the assistant's answer.
    """
    # Prepare the conversation entry
    conversation_entry = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "timestamp": datetime.utcnow(),
        "user_message": user_message,
        "assistant_answer": assistant_answer
    }
    
    # Insert the conversation entry into MongoDB
    collection.insert_one(conversation_entry)
    
    return assistant_answer

def start_new_conversation(user_id):
    """
    Starts a new conversation for a user and returns the conversation ID.
    """
    conversation_id = str(uuid4())  # Generate a unique ID for the conversation
    return conversation_id
