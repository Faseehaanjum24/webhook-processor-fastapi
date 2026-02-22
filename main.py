from fastapi import FastAPI, BackgroundTasks, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from redis import Redis
from urllib.parse import urlparse
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Parse Redis URL
redis_url = os.getenv("REDIS_URL")
parsed = urlparse(redis_url)

redis_client = Redis(
    host=parsed.hostname,
    port=parsed.port,
    password=parsed.password,
    username=parsed.username,
    ssl=True
)

class Transaction(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

def process_transaction(data: dict):
    txid = data["transaction_id"]
    key = f"txn:{txid}"

    # Idempotency lock
    if redis_client.exists(f"{key}:lock"):
        return

    redis_client.set(f"{key}:lock", 1)

    # Mark as PROCESSING
    redis_client.hset(key, mapping={
        "status": "PROCESSING",
        "created_at": datetime.utcnow().isoformat(),
         
    })

    time.sleep(30)

    # Mark as PROCESSED
    redis_client.hset(key, mapping={
        "status": "PROCESSED",
        "processed_at": datetime.utcnow().isoformat()
    })

@app.get("/")
def health():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat()
    }

@app.post("/v1/webhooks/transactions", status_code=status.HTTP_202_ACCEPTED)
def receive_webhook(payload: Transaction, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_transaction, payload.dict())
    return JSONResponse(
        content={"message": "Webhook received"},
        status_code=status.HTTP_202_ACCEPTED
    )

@app.get("/v1/transactions/{transaction_id}")
def transaction_status(transaction_id: str):
    key = f"txn:{transaction_id}"
    txn = redis_client.hgetall(key)

    if not txn:
        return []

    return [{
        k.decode(): v.decode()
        for k, v in txn.items()
    }]