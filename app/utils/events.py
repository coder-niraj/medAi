import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, ServiceUnavailable

# Force the library to use the local emulator
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
os.environ["GOOGLE_CLOUD_PROJECT"] = "med-ai-project"

publisher = pubsub_v1.PublisherClient()
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def init_pubsub():
    topic_id = "new-report-uploaded"
    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        publisher.create_topic(name=topic_path)
        print(f"✅ Pub/Sub Topic Created: {topic_id}")
    except AlreadyExists:
        print(f"ℹ️ Topic {topic_id} already exists.")
    except Exception as e:
        print(f"⚠️ Could not connect to Pub/Sub Emulator: {e}")
        print("Check if the Docker container 'medai-pubsub-local' is running.")
