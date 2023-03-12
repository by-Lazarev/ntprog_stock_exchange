from __future__ import annotations

from fastapi import HTTPException
import asyncio
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from random import randint

from schemas import OrderBase
from enums import *
from handlers.task_handlers import *
from models.server_messages import *


if TYPE_CHECKING:
    import fastapi

    from server.models import client_messages
    from server.ntpro_server import NTProServer


async def subscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.SubscribeMarketData,
):
    current_connection = server.connections[websocket.client]
    new_id = create_id()
    current_connection.subscriptions.append(asyncio.create_task(subscribe_handler(), name=str(new_id)))
    response = response_handler(
        MessageType.SuccessInfo,
        SuccessInfo(subscriptionId=new_id)
    )
    return response


async def unsubscribe_market_data_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.UnsubscribeMarketData,
):
    current_connection = server.connections[websocket.client]
    task = None
    for task in current_connection.subscriptions:
        if task.get_name() == message.subscription_id:
            break
    if task is None:
        response = response_handler(
            MessageType.ErrorInfo,
            ErrorInfo(reason="There is not task with this uuid")
        )
    else:
        current_connection.subscriptions.remove(task)
        task.cancel()
        response = response_handler(
            MessageType.SuccessInfo,
            SuccessInfo(subscriptionId=message.subscription_id)
        )

    return response


async def place_order_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.PlaceOrder,
):
    new_order = OrderBase(
        creation_time=datetime.now(),
        change_time=datetime.now(),
        status=OrderStatus.active,
        side=OrderSide(message.side),
        price=message.price,
        amount=message.amount,
        instrument=Instrument(message.instrument)
    )
    new_id = create_id()
    # add db connection -> add, commit, refresh
    response = response_handler(
        MessageType.SuccessInfo,
        SuccessInfo(orderId=new_id)
    )

    return response


def cancel_order_processor():
    pass
