import redis
import json
import time
import os
from collections import Counter

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

worker_name = os.getenv("HOSTNAME", "worker")

keywords = ["python", "docker", "fastapi", "redis", "cloud", "aws", "javascript","Messi","Chivas"]

def analyze_text(text):
    words = text.lower().split()

    word_count = len(words)
    char_count = len(text)

    most_common = Counter(words).most_common(5)

    found_keywords = []
    for word in words:
        clean_word = word.strip(".,;:!?¿¡()[]{}")
        if clean_word in keywords and clean_word not in found_keywords:
            found_keywords.append(clean_word)

    return {
        "worker": worker_name,
        "Conteo de Palabras": word_count,
        "Conteo de caracteres": char_count,
        "Palabras mas frecuentes": most_common,
        "Palabras clave encontradas": found_keywords
    }

print(f"{worker_name} esperando tareas...")

while True:
    task = redis_client.brpop("task_queue")

    if task:
        task_id = task[1]

        task_data = redis_client.get(f"task:{task_id}")

        if task_data:
            data = json.loads(task_data)

            try:
                data["status"] = "en proceso"
                redis_client.set(f"task:{task_id}", json.dumps(data))

                print(f"{worker_name} procesando tarea {task_id}")

                time.sleep(4)

                result = analyze_text(data["text"])

                data["status"] = "completada"
                data["result"] = result

                redis_client.set(f"task:{task_id}", json.dumps(data))

                print(f"{worker_name} completó tarea {task_id}")

            except Exception as error:
                data["status"] = "error"
                data["result"] = str(error)

                redis_client.set(f"task:{task_id}", json.dumps(data))
