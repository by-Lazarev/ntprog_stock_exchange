from sqlalchemy.orm.session import Session

from schemas import OrderBase
from db.models import DbOrder
from handlers.task_handlers import *
from handlers.task_handlers import response_handler
from models.server_messages import *


def create_order(db: Session, request: OrderBase):
    new_order = DbOrder(
        creation_time=request.creation_time,
        change_time=request.change_time,
        status=StatusHandler().status_to_int(request.status),
        side=request.side,
        price=request.price,
        amount=request.amount,
        instrument=request.status,
        uuid=request.uuid,
        user_id=request.user_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def delete_order(db: Session, order_uuid: uuid.UUID, user_id: id):
    order = db.query(DbOrder).filter(DbOrder.uuid == order_uuid).first()
    if not order:
        return response_handler(
            MessageType.ErrorInfo,
            ErrorInfo(reason="There are no order with this uuid")
        )
    if order.user_id != user_id:
        return response_handler(
            MessageType.ErrorInfo,
            ErrorInfo(reason="You are not allowed to delete other's order")
        )
    db.delete(order)
    db.commit()
    return response_handler(
        MessageType.SuccessInfo,
        SuccessInfo(orderId=order_uuid)
    )
