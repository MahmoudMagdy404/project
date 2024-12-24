import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
FIREBASE_CREDENTIALS = "firebase_config.json"  # Path to Firebase credentials

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit(1)

# Firestore Client
db = firestore.client()

def insert_document(agent_id, password, role):
    """
    Insert a document into the 'agents' collection.
    """
    try:
        db.collection('agents').document(agent_id).set({
            'password': password,
            'role': role
        })
        print(f"Document with Agent ID '{agent_id}' added successfully.")
    except Exception as e:
        print(f"Error inserting document: {e}")

def fetch_document(agent_id):
    """
    Fetch a document from the 'agents' collection.
    """
    try:
        doc = db.collection('agents').document(agent_id).get()
        if doc.exists:
            print("Document found!")
            print("Data:", doc.to_dict())
        else:
            print("Document does not exist!")
    except Exception as e:
        print(f"Error fetching document: {e}")

if __name__ == "__main__":
    print("Firestore CLI - Insert and Fetch Documents")
    print("Options:")
    print("1. Insert Document")
    print("2. Fetch Document")
    print("3. Exit")

    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            agent_id = input("Enter Agent ID: ").strip()
            password = input("Enter Password: ").strip()
            role = input("Enter Role (TL/agent): ").strip()
            insert_document(agent_id, password, role)

        elif choice == "2":
            agent_id = input("Enter Agent ID to fetch: ").strip()
            fetch_document(agent_id)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
