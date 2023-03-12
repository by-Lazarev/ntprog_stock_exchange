from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy import Column
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import Integer, String
from pydantic import BaseModel

from db.database import get_db, Base

router = APIRouter(
    prefix="/db_test",
    tags=["db_test"]
)


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


@router.post("/", response_model=UserDisplay)
def post_user(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)


@router.get("/", response_model=list[UserDisplay])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)
