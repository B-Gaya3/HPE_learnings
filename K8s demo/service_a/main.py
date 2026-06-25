from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello from Service A!", "service": "A"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "A"}
