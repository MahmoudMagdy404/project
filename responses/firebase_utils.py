import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    cred = credentials.Certificate(Path(__file__).parent.parent / 'firebase_config.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

def get_agent_by_id(agent_id):
    """Retrieve agent data from Firestore"""
    db = firestore.client()
    agent_doc = db.collection('agents').document(agent_id).get()
    return agent_doc.to_dict() if agent_doc.exists else None

def save_response_data(data):
    """Save response data to Firestore"""
    db = firestore.client()
    return db.collection('response_data').add(data)