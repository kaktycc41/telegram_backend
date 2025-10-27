# backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets, time

app = FastAPI()
AGENTS = {}
PENDING = {}

class PairResponse(BaseModel):
    token: str

class Task(BaseModel):
    type: str
    params: dict

@app.post("/pair", response_model=PairResponse)
def pair():
    token = secrets.token_urlsafe(16)
    AGENTS[token] = {'last_seen': time.time()}
    PENDING[token] = []
    return {"token": token}

@app.get("/tasks/{token}")
def get_tasks(token: str):
    if token not in AGENTS:
        raise HTTPException(status_code=404, detail="Token not found")
    AGENTS[token]['last_seen'] = time.time()
    tasks = PENDING.get(token, [])
    PENDING[token] = []
    return {"tasks": tasks}

@app.post("/task/{token}")
def create_task(token: str, task: Task):
    if token not in AGENTS:
        raise HTTPException(status_code=404, detail="Token not found")
    PENDING[token].append(task.dict())
    return {"ok": True}
