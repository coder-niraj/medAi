import asyncio
import json
from contextlib import asynccontextmanager
from google.cloud import pubsub_v1
from tasks.index import init_pubsub
from fastapi import FastAPI
async def pubsub_subscriber_task():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("med-ai-project", "process-report-sub")
    print("here subscriber listened")

    def callback(message):
        print("message callback is hit")
        try:
            data = json.loads(message.data.decode("utf-8"))
            print("your data : ",data)
            message.ack()
        except Exception as e:
            print("error occurred in callback")
            message.nack()
    with subscriber:
        streaming_pull_future =subscriber.subscribe(subscription_path,callback=callback)
        print("🚀 Pub/Sub Listener Started...")
        try:
            await asyncio.wrap_future(streaming_pull_future)
        except asyncio.CancelledError:
            streaming_pull_future.cancel()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ON STARTUP ---
    # 1. Initialize topics and subscriptions
    init_pubsub() 
    
    # 2. Create the background task
    task = asyncio.create_task(pubsub_subscriber_task())
    
    yield  # FastAPI runs here
    
    # --- ON SHUTDOWN ---
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("🛑 Pub/Sub Listener Stopped")
