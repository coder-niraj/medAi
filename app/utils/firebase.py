import os
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

from services.kms import KMSService

# Ensure the correct .env path is loaded
load_dotenv()

def initialize_firebase():
    if not firebase_admin._apps:
        firebase_creds = KMSService.get_secret("FIREBASE_CREDENTIALS")
        # The SDK specifically looks for these exact keys
        cert_dict = {
            "type": "service_account",  # THIS IS THE MISSING KEY
            "project_id": firebase_creds["FIREBASE_PROJECT_ID"],
            "private_key_id": firebase_creds["FIREBASE_PRIVATE_KEY_ID"],
            "private_key": firebase_creds["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),
            "client_email": firebase_creds["FIREBASE_CLIENT_EMAIL"],
            "auth_uri": firebase_creds["auth_uri"],
            "token_uri": firebase_creds["token_uri"],
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{firebase_creds['FIREBASE_CLIENT_EMAIL'].replace('@', '%40')}"
        }

        try:
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")

# Run the initialization
initialize_firebase()

def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Firebase Token Verification Error: {e}")
        return None