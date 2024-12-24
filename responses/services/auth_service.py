from responses.firebase_utils import db

def authenticate_agent(name, password):
    """Authenticate an agent using Firestore."""
    try:
        name = name.strip()  # Clean input
        print(f"Fetching document for Name: '{name}'")  # Debugging

        doc = db.collection('agents').document(name).get()
        if doc.exists:
            agent_data = doc.to_dict()
            print(f"Fetched Data for Name '{name}': {agent_data}")

            # Compare the password
            if agent_data.get('password') == password:
                print("Password match successful.")
                role = agent_data.get('role', 'agent')  # Default to 'agent' if no role
                id = agent_data.get('id')  # Retrieve the id field
                return True, role, id  # Return role and ID
            else:
                print("Password mismatch.")
        else:
            print("Document does not exist.")

        return False, None, None 
    except Exception as e:
        print(f"Error in authenticate_agent: {e}")
        return False, None, None

