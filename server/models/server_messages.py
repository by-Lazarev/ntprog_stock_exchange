from __future__ import annotations

import uuid
from typing import TypeVar

import bidict as bidict

import enums
from enum import Enum
from models.base import Envelope, Message, Quote


class MessageType(Enum):
    SubscribeMarketData: int = 1
    UnsubscribeMarketData: int = 2
    PlaceOrder: int = 3
    CancelOrder: int = 4
    SuccessInfo: int = 5
    ErrorInfo: int = 6


class ServerMessage(Message):
    def get_type(self: ServerMessageT) -> enums.ServerMessageType:
        return _SERVER_MESSAGE_TYPE_BY_CLASS[self.__class__]


class ErrorInfo(ServerMessage):
    reason: str


class SuccessInfo(ServerMessage):
    subscriptionId: uuid.UUID | None = None
    orderId: uuid.UUID | None = None


class ExecutionReport(ServerMessage):
    order_id: uuid.UUID
    order_status: enums.OrderStatus


class MarketDataUpdate(ServerMessage):
    subscription_id: uuid.UUID
    instrument: enums.Instrument
    quotes: list[Quote]


class ServerEnvelope(Envelope):
    message_type: enums.ServerMessageType

    def get_parsed_message(self):
        return _SERVER_MESSAGE_TYPE_BY_CLASS.inverse[self.message_type].parse_obj(self.message)


_SERVER_MESSAGE_TYPE_BY_CLASS = bidict.bidict({
    SuccessInfo: enums.ServerMessageType.success,
    ErrorInfo: enums.ServerMessageType.error,
    ExecutionReport: enums.ServerMessageType.execution_report,
    MarketDataUpdate: enums.ServerMessageType.market_data_update,
})
ServerMessageT = TypeVar('ServerMessageT', bound=ServerMessage)
