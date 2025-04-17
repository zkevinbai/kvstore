from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()
store = {}


class KeyValue(BaseModel):
    key: str
    value: str


@app.get("/get/{key}")
def get_value(key: str):
    if key in store:
        return {"key": key, "value": store[key]}
    raise HTTPException(status_code=404, detail="Key not found")


@app.post("/set")
def set_value(kv: KeyValue):
    store[kv.key] = kv.value
    return {"message": f"Key '{kv.key}' set successfully."}


@app.delete("/delete/{key}")
def delete_value(key: str):
    if key in store:
        del store[key]
        return {"message": f"Key '{key}' deleted successfully."}
    raise HTTPException(status_code=404, detail="Key not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
