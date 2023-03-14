import uuid
from uuid import uuid4
from asyncio import sleep
from random import randint

from enums import OrderStatus

id_storage = set()


class StatusHandler:
    statuses = [OrderStatus.active,
                OrderStatus.filled,
                OrderStatus.rejected]

    def create_status(self):
        return self.statuses[randint(0, 2)]

    def status_to_int(self, status):
        try:
            return self.statuses.index(status) + 1
        except ValueError:
            return 3


def get_current_user(client):
    return 1


def create_id() -> uuid.UUID:
    new_id = uuid4()
    while new_id in id_storage:
        new_id = uuid4()
    id_storage.add(new_id)
    return new_id


async def subscribe_handler():
    await sleep(randint(0, 2))


def response_handler(response_type: int, message: object) -> dict:
    response = {
        "messageType": response_type,
        "message": message
    }
    return response
