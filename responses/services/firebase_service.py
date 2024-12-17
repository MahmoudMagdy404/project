"""
Firebase service layer handling all Firebase operations
"""
import firebase_admin
from firebase_admin import credentials, firestore
from ..config import FIREBASE_CONFIG_PATH

def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(str(FIREBASE_CONFIG_PATH))
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        raise

def get_firestore_client():
    """Get Firestore client, ensuring Firebase is initialized"""
    if not firebase_admin._apps:
        initialize_firebase()
    return firestore.client()

def get_agent_by_id(agent_id):
    """Retrieve agent data from Firestore"""
    try:
        db = get_firestore_client()
        agent_doc = db.collection('agents').document(agent_id).get()
        return agent_doc.to_dict() if agent_doc.exists else None
    except Exception as e:
        print(f"Error retrieving agent: {e}")
        return None

def save_response_data(data):
    """Save response data to Firestore"""
    try:
        db = get_firestore_client()
        return db.collection('response_data').add(data)
    except Exception as e:
        print(f"Error saving response: {e}")
        raise

def get_all_responses():
    """Retrieve all responses from Firestore"""
    try:
        db = get_firestore_client()
        responses = db.collection('response_data').get()
        return [{'id': doc.id, **doc.to_dict()} for doc in responses]
    except Exception as e:
        print(f"Error retrieving responses: {e}")
        return []