## Transaction Webhook Processor (FastAPI + Redis)

This service receives transaction webhooks, responds immediately with 202 Accepted, and processes them in the background using Redis. Processing includes a 30-second simulated delay, while the API remains fast and responsive.

## Public Deployment:
https://webhook-processor-v1cr.onrender.com

## Features

1 - FastAPI-based webhook service
2 - Background processing using FastAPI BackgroundTasks
3 - 30-second simulated processing delay
4 - Idempotent: each transaction_id is processed only once
5 - Redis used as persistent storage
6 - Fast API response (<500ms)
7 - Transaction status polling support



## API Endpoints

1. Health Check

GET /
Example Response:

{
  "status": "HEALTHY",
  "current_time": "2024-01-15T10:30:00Z"
}


2. Receive Webhook

POST /v1/webhooks/transactions

Example Request:

{
  "transaction_id": "txn_abc123",
  "source_account": "A",
  "destination_account": "B",
  "amount": 1500,
  "currency": "INR"
}

Example Response:

{
  "message": "Webhook received"
}


3. Get Transaction Status

GET /v1/transactions/{transaction_id}

While processing:

[
  {
    "status": "PROCESSING",
    "created_at": "2026-02-22T13:49:04.943633"
  }
]

After processing completes (~30 seconds):

[
  {
    "status": "PROCESSED",
    "created_at": "2026-02-22T13:49:04.943633",
    "processed_at": "2026-02-22T13:49:34.943900"
  }
]


## GitHub Repository

 
https://github.com/Faseehaanjum24/webhook-processor-fastapi


----


## Live Deployed API (Render)
Base URL: https://webhook-processor-v1cr.onrender.com

Health: https://webhook-processor-v1cr.onrender.com/

Swagger Docs: https://webhook-processor-v1cr.onrender.com/docs

Webhook Endpoint: POST /v1/webhooks/transactions
Status Endpoint: GET /v1/transactions/{id}