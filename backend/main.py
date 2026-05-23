from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import redis
import uuid
import json
import time

app = FastAPI()

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextTask(BaseModel):
    text: str

@app.get("/")
async def home():
    return {"message": "API funcionando correctamente"}

@app.post("/tasks")
async def create_task(task: TextTask):
    task_id = str(uuid.uuid4())

    data = {
        "id": task_id,
        "text": task.text,
        "status": "pendiente",
        "result": None
    }

    redis_client.set(f"task:{task_id}", json.dumps(data))
    redis_client.lpush("task_queue", task_id)

    return {
        "id": task_id,
        "status": "pendiente"
    }

@app.get("/tasks")
async def get_tasks():
    keys = redis_client.keys("task:*")
    tasks = []

    for key in keys:
        task_data = redis_client.get(key)
        if task_data:
            tasks.append(json.loads(task_data))

    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task_data = redis_client.get(f"task:{task_id}")

    if not task_data:
        return {"error": "Tarea no encontrada"}

    return json.loads(task_data)

@app.get("/events/{task_id}")
async def task_events(task_id: str):
    def event_stream():
        last_status = None

        while True:
            task_data = redis_client.get(f"task:{task_id}")

            if task_data:
                task = json.loads(task_data)
                current_status = task["status"]

                if current_status != last_status:
                    yield f"data: {json.dumps(task)}\n\n"
                    last_status = current_status

                if current_status in ["completada", "error"]:
                    break

            time.sleep(1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
