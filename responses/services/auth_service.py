from responses.firebase_utils import db

def authenticate_agent(agent_id, password):
    """Authenticate an agent using Firestore."""
    try:
        agent_id = agent_id.strip()  # Clean input
        print(f"Fetching document for Agent ID: '{agent_id}'")  # Debugging

        doc = db.collection('agents').document(agent_id).get()
        if doc.exists:
            agent_data = doc.to_dict()
            print(f"Fetched Data: {agent_data}")
            
            # Compare the password
            if agent_data.get('password') == password:
                print("Password match successful.")
                return True, agent_data.get('role', 'agent')  # Default role: 'agent'
            else:
                print("Password mismatch.")
        else:
            print("Document does not exist.")

        return False, None
    except Exception as e:
        print(f"Error in authenticate_agent: {e}")
        return False, None
