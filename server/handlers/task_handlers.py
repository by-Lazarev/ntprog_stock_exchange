import uuid
from uuid import uuid4
import asyncio

id_storage = set()


def create_id() -> uuid.UUID:
    new_id = uuid4()
    while new_id in id_storage:
        new_id = uuid4()
    id_storage.add(new_id)
    return new_id


async def subscribe_handler():
    await asyncio.sleep(1)


def response_handler(response_type: int, message: object) -> dict:
    response = {
        "messageType": response_type,
        "message": message
    }
    return response
