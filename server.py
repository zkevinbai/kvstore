from fastapi import FastAPI, HTTPException, Request, Depends, Header
from pydantic import BaseModel
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import logging
import uvicorn
import json
import os

app = FastAPI()
store = {}
request_log = {} 

DATA_FILE = 'data.json'
RATE_LIMIT = 5
WINDOW_SECONDS = 60
API_KEY = 'apikey'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
class KeyValue(BaseModel):
    key: str
    value: str

def save_store():
    with open(DATA_FILE, 'w') as f:
        json.dump(store, f)

def load_store():
    global store
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            store = json.load(f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_store()
    yield
    save_store()

app = FastAPI(lifespan=lifespan)

def rate_limiter(request: Request):
    client_ip = request.client.host
    # now = datetime.now(datetime.UTC)
    now = datetime.utcnow()

    # Log each incoming request
    logger.info(f"[RATE LIMIT] IP: {client_ip} at {now.isoformat()}")

    times_called = request_log.get(client_ip, [])

    times_called = [t for t in times_called if now - t < timedelta(seconds=WINDOW_SECONDS)]
    times_called.append(now)

    request_log[client_ip] = times_called

    if len(times_called) > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded, more than 5 requests per minute")

def authenticate_user(incoming_api_key: str = Header(...)):
    if incoming_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing api key")


@app.get("/get/{key}")
def get_value(key: str, __: None = Depends(authenticate_user)):
    if key in store:
        return {"key": key, "value": store[key]}
    raise HTTPException(status_code=404, detail="Key not found")


@app.post("/set")
def set_value(kv: KeyValue, _: None = Depends(rate_limiter), __: None = Depends(authenticate_user)):
    store[kv.key] = kv.value
    save_store()
    return {"message": f"Key '{kv.key}' set successfully."}


@app.delete("/delete/{key}")
def delete_value(key: str, _: None = Depends(rate_limiter), __: None = Depends(authenticate_user)):
    if key in store:
        del store[key]
        save_store()
        return {"message": f"Key '{key}' deleted successfully."}
    raise HTTPException(status_code=404, detail="Key not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
