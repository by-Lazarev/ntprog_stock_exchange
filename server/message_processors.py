from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING

from enums import *
from db.db_order import *
from db.database import get_db


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
    new_id = create_id()
    current_connection = server.connections[websocket.client]
    current_user = get_current_user(current_connection)
    order_status = StatusHandler().create_status()
    new_order = OrderBase(
        creation_time=datetime.now(),
        change_time=datetime.now(),
        status=order_status,
        side=OrderSide(message.side),
        price=message.price,
        amount=message.amount,
        instrument=Instrument(message.instrument),
        user_id=current_user,
        uuid=str(new_id)
    )
    create_order(get_db(), new_order)
    response = response_handler(
        MessageType.SuccessInfo,
        SuccessInfo(orderId=new_id)
    )

    return response


def cancel_order_processor(
        server: NTProServer,
        websocket: fastapi.WebSocket,
        message: client_messages.CancelOrder
):
    current_connection = server.connections[websocket.client]
    current_user = get_current_user(current_connection)
    db = get_db()
    response = delete_order(db, message.order_uuid, current_user)
    return response
