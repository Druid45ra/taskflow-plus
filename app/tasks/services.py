import json
from ..core.websocket_manager import manager

async def send_task_update(task_data: dict, user_id: int):
    message = json.dumps({
        "event_type": "TASK_UPDATE",
        "data": task_data
    })
    await manager.send_personal_message(message, user_id)

async def broadcast_task_creation(task_data: dict):
    message = json.dumps({
        "event_type": "TASK_CREATED",
        "data": task_data
    })
    await manager.broadcast(message)

async def send_task_notification(task_data: dict, user_id: int):
    message = json.dumps({
        "event_type": "TASK_NOTIFICATION",
        "data": task_data
    })
    await manager.send_personal_message(message, user_id)
