import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "med-ai-project")


def init_pubsub():
    publisher = pubsub_v1.PublisherClient()

    topic_id = "new-report-uploaded"
    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        publisher.create_topic(request={"name": topic_path})
        print("✅ Topic created")

    except AlreadyExists:
        print("ℹ️ Topic already exists")

    except Exception as e:
        print("⚠️ PubSub failed:", e)
