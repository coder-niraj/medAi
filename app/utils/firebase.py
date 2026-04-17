import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env

def initialize_firebase():
    # Check if Firebase is already initialized to avoid errors
    if not firebase_admin._apps:
        # Construct the credential dictionary from environment variables
        cred_dict = {
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'), # Fixes newline issues
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

initialize_firebase()