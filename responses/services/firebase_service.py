from responses.firebase_utils import db

def get_agent_by_id(agent_id):
    """Retrieve agent data from Firestore"""
    try:
        agent_doc = db.collection('agents').document(agent_id).get()
        return agent_doc.to_dict() if agent_doc.exists else None
    except Exception as e:
        print(f"Error retrieving agent: {e}")
        raise

def save_response_data(data):
    """Save response data to Firestore"""
    try:
        return db.collection('response_data').add(data)
    except Exception as e:
        print(f"Error saving response: {e}")
        raise

from responses.firebase_utils import db

def get_all_responses():
    """Retrieve all responses and resolve agent_name."""
    try:
        responses = db.collection('response_data').get()
        agents = {doc.id: doc.to_dict().get('name', 'Unknown') for doc in db.collection('agents').stream()}
        
        response_list = []
        for doc in responses:
            data = doc.to_dict()
            data['agent_name'] = agents.get(data.get('agent_id'), 'Unknown')  # Resolve agent_name
            response_list.append({'id': doc.id, **data})
        
        return response_list
    except Exception as e:
        print(f"Error retrieving responses: {e}")
        return []


def add_user_to_firestore(agent_id, password, role):
    """Add a new user to the 'agents' collection in Firestore"""
    try:
        doc_ref = db.collection('agents').document(agent_id)
        doc_ref.set({
            'password': password,
            'role': role
        })
        print(f"User '{agent_id}' added to Firestore successfully.")
    except Exception as e:
        
        print(f"Error adding user to Firestore: {e}")
        raise
    
import random
import string
from responses.firebase_utils import db

def get_last_agent_id():
    """Fetch the highest agent ID from the agents collection."""
    try:
        agents = db.collection('agents').stream()
        ids = [doc.to_dict().get('id', 0) for doc in agents]  # Get 'id' field
        return max(ids) if ids else 0
    except Exception as e:
        print(f"Error fetching last agent ID: {e}")
        return 0


def generate_random_password(length=8):
    """Generate a random unique password."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_new_user(name, role):
    """Generate a new user with a unique ID and random password."""
    try:
        last_id = get_last_agent_id()
        new_id = last_id + 1  # Increment the last ID
        password = generate_random_password()

        # Add user to Firestore using 'name' as document ID
        db.collection('agents').document(name).set({
            'id': new_id,  # Store the ID as a field
            'password': password,
            'role': role
        })

        return new_id, password
    except Exception as e:
        print(f"Error generating new user: {e}")
        raise


