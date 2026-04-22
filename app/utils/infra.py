import os
from google.cloud import storage
from google.cloud import kms_v1 as kms
from google.auth import credentials
import grpc # Make sure to: pip install grpcio
from google.api_core.client_options import ClientOptions
# IMPORTANT: These must be set BEFORE the clients are initialized
os.environ["STORAGE_EMULATOR_HOST"] = "http://127.0.0.1:8000"
os.environ["KMS_EMULATOR_HOST"] = "127.0.0.1:8001"

def bootstrap_local_infra():
    project_id = "medai-project"
    anon_creds = credentials.AnonymousCredentials()
    
    print("🚀 Starting Infrastructure Bootstrap...")

    # --- 1. SETUP STORAGE ---
    try:
        # Using a timeout and explicit anonymous credentials
        storage_client = storage.Client(
            project=project_id, 
            credentials=anon_creds
        )
        
        bucket_name = "medical-reports"
        # list_buckets can be slow on Windows Docker, so we try a direct get
        try:
            storage_client.get_bucket(bucket_name)
            print(f"ℹ️ Bucket '{bucket_name}' already exists.")
        except:
            storage_client.create_bucket(bucket_name)
            print(f"✅ Bucket '{bucket_name}' created successfully.")
            
    except Exception as e:
        print(f"❌ Storage Error: {e}")

    # --- 2. SETUP KMS ---
    try:
        # THE FIX: Ensure credentials=anon_creds is passed inside the constructor
#         kms_client = kms.KeyManagementServiceClient(
#     client_options={"api_endpoint": "127.0.0.1:8001"},
#     credentials=anon_creds 
# )
        channel = grpc.insecure_channel("127.0.0.1:8001")

        # Create the transport with the channel and credentials inside it
        transport = kms.services.key_management_service.transports.KeyManagementServiceGrpcTransport(
            channel=channel,
            credentials=anon_creds
        )

        # Initialize the client using ONLY the transport
        kms_client = kms.KeyManagementServiceClient(transport=transport)
        
        location_path = f"projects/{project_id}/locations/global"
        key_ring_id = "medai-key-ring"
        key_id = "data-encryption-key"
        key_ring_path = f"{location_path}/keyRings/{key_ring_id}"  
      

        # Create KeyRing
        try:
            kms_client.get_key_ring(name=key_ring_path)
            print(f"ℹ️ KeyRing '{key_ring_id}' exists.")
        except Exception:
            kms_client.create_key_ring(parent=location_path, key_ring_id=key_ring_id)
            print(f"✅ KeyRing '{key_ring_id}' created.")

        # Create CryptoKey
        key_path = f"{key_ring_path}/cryptoKeys/{key_id}"
        try:
            kms_client.get_crypto_key(name=key_path)
            print(f"ℹ️ CryptoKey '{key_id}' exists.")
        except Exception:
            purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
            crypto_key = {"purpose": purpose}
            kms_client.create_crypto_key(parent=key_ring_path, crypto_key_id=key_id, crypto_key=crypto_key)
            print(f"✅ CryptoKey '{key_id}' created.")

    except Exception as e:
        print(f"❌ KMS Error: {e}")

if __name__ == "__main__":
    bootstrap_local_infra()