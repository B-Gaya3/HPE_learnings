import os
import httpx
from fastapi import FastAPI

app = FastAPI()

# In manual mode: hardcoded IP. In K8s: use service name.
SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://localhost:8001")

@app.get("/")
async def hello():
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{SERVICE_A_URL}/")
            a_data = resp.json()
    except Exception as e:
        a_data = {"error": str(e)}

    return {
        "message": "Hello from Service B!",
        "service": "B",
        "service_a_says": a_data
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "B"}
