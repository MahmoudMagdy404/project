import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Path to Firebase credentials
FIREBASE_CREDENTIALS = Path(__file__).resolve().parent.parent / 'firebase_config.json'

# Initialize Firebase App
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(str(FIREBASE_CREDENTIALS))
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        raise

# Firestore DB instance
db = firestore.client()
