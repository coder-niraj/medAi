import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

from services.kms import KMSService

project_id = KMSService.get_secret("GCP_PROJECT_ID")


def init_pubsub():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_id = "new-report-uploaded"
    sub_id = "process-report-sub"
    topic_path = publisher.topic_path(project_id, topic_id)
    sub_path = subscriber.subscription_path(project_id, sub_id)

    try:
        publisher.create_topic(request={"name": topic_path})
        print("✅ Topic created")

    except AlreadyExists:
        print("ℹ️ Topic already exists")

    except Exception as e:
        print("⚠️ Pub failed:", e)

    try:
        subscriber.create_subscription(request={"name": sub_path, "topic": topic_path})
        print("✅ Subscription created")
    except AlreadyExists:
        print("ℹ️ Subscription already exists")
    except Exception as e:
        print("⚠️ Sub failed:", e)