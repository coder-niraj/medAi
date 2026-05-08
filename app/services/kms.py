# services/kms.py
import os
import requests
from functools import lru_cache

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://medai-vault:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "dev-root-token")

import time
import hvac  # type: ignore


class KMSService:
    @staticmethod
    def get_secret(secret_name, max_retries=10):
        client = hvac.Client(url="http://medai-vault:8200", token="dev-root-token")

        for i in range(max_retries):
            try:
                # Attempt to read the secret
                read_response = client.secrets.kv.v2.read_secret_version(
                    path=secret_name
                )
                if secret_name == "FIREBASE_CREDENTIALS":
                    return read_response["data"]["data"]
                else:
                    return read_response["data"]["data"]["value"]
            except Exception:
                print(
                    f"⏳ Secret '{secret_name}' not ready yet... retrying ({i+1}/{max_retries})"
                )
                time.sleep(2)  # Wait 2 seconds before trying again

        raise ValueError(f"Secret not found after retrying: {secret_name}")
