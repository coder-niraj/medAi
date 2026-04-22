import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class AES256Service:
    """
    HIPAA-compliant AES-256 GCM Encryption Service.
    Standardizes PII protection for Email, Phone, and DOB.
    """
    # In production, this key should come from an environment variable 
    # or Google Cloud Secret Manager (KMS)
    _MASTER_KEY = os.getenv("DB_ENCRYPTION_KEY", "your-super-secret-32-byte-key-here!!")

    @classmethod
    def encrypt(cls, plain_text: str) -> str:
        if not plain_text:
            return None
        
        aesgcm = AESGCM(cls._MASTER_KEY.encode()[:32]) # Ensure 256-bit
        nonce = os.urandom(12) # GCM standard nonce length
        
        ciphertext = aesgcm.encrypt(nonce, plain_text.encode(), None)
        
        # Combine nonce + ciphertext and encode to base64 for DB storage
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    @classmethod
    def decrypt(cls, encrypted_text: str) -> str:
        if not encrypted_text:
            return None
            
        data = base64.b64decode(encrypted_text.encode('utf-8'))
        nonce = data[:12]
        ciphertext = data[12:]
        
        aesgcm = AESGCM(cls._MASTER_KEY.encode()[:32])
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        
        return decrypted_data.decode('utf-8')