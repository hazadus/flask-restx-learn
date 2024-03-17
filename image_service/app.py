"""
docker run -p 6379:6379 --name my-redis -d redis
curl -X POST  -H "Content-Type: application/json" --data '{"images": ["image1", "image2", "image3"]}' http://127.0.0.1:5000/process_images
"""

import random

from flask import Flask, request, jsonify
from celery import Celery, group
import time

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
    app.name,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@celery.task
def process_image(image_id: str):
    time.sleep(random.randint(5, 15))
    return f"Image {image_id} processed"


@app.route("/process_images", methods=["POST"])
def process_images():
    images = request.json.get("images")

    if images and isinstance(images, list):
        # Создаём группу задач
        task_group = group(process_image.s(image_id) for image_id in images)

        # Запускаем группу задач и сохраняем её
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({"group_id": result.id}), 202
    else:
        return jsonify({"error": "Missing or invalid images parameter"}), 400


@app.route("/status/<group_id>", methods=["GET"])
def get_group_status(group_id: str):
    result = celery.GroupResult.restore(group_id)

    if result:
        status = result.completed_count() / len(result)
        return jsonify({"status": status}), 200
    else:
        return jsonify({"error": "Invalid group_id"}), 404


if __name__ == "__main__":
    app.run(debug=True)
