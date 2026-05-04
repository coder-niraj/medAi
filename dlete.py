import requests

BASE_URL = "http://localhost:8000"
BUCKET = "med-ai-reports"

# 1. Get all objects
list_url = f"{BASE_URL}/storage/v1/b/{BUCKET}/o"

response = requests.get(list_url)
data = response.json()

items = data.get("items", [])

# 2. Delete each object
for obj in items:
    file_name = obj["name"]

    delete_url = f"{BASE_URL}/storage/v1/b/{BUCKET}/o/{file_name}"

    r = requests.delete(delete_url)

    print(f"Deleted: {file_name} -> {r.status_code}")

print("All files deleted.")
