import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from mqtt_emitter import mqtt_emitter
from mqtt_processor import mqtt_processor

# Initialize FastAPI app
app = FastAPI()

# MongoDB Client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Data model for querying message counts
class TimeRange(BaseModel):
    start_time: str
    end_time: str

def count_statuses(start_time: str, end_time: str) -> Dict[str, int]:
    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": datetime.fromisoformat(start_time),
                    "$lte": datetime.fromisoformat(end_time)
                }
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]
    result = collection.aggregate(pipeline)
    return {str(doc["_id"]): doc["count"] for doc in result}

@app.post("/status_counts")
def get_status_counts(time_range: TimeRange):
    try:
        counts = count_statuses(time_range.start_time, time_range.end_time)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lifespan to manage threads
@app.on_event("startup")
def start_mqtt_threads():
    emitter_thread = threading.Thread(target=mqtt_emitter, daemon=True)
    processor_thread = threading.Thread(target=mqtt_processor, daemon=True)

    emitter_thread.start()
    processor_thread.start()

@app.on_event("shutdown")
def stop_mqtt_threads():
    print("[INFO] Shutting down MQTT threads...")
    # Threads are daemonized, so they will exit automatically when the app stops.
