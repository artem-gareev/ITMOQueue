from datetime import datetime

from database.models import User, Queue, PersonsInQueue
from typing import Optional
from database.database import SessionLocal


def create_user(telegram_id: int, username: Optional[str]) -> User:
    session = SessionLocal()
    db_user = User(
        telegram_id=telegram_id, name=username,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_queue(name: str) -> Queue:
    session = SessionLocal()
    db_queue = Queue(
        name=name,
    )
    session.add(db_queue)
    session.commit()
    session.refresh(db_queue)
    return db_queue


def get_all_queues():
    session = SessionLocal()
    return session.query(Queue).all()


def get_queue_persons(queue_id: int) -> list[PersonsInQueue]:
    session = SessionLocal()
    return session.query(PersonsInQueue).filter(PersonsInQueue.queue_id == queue_id).order_by(
        PersonsInQueue.enter_date).all()


def get_user(telegram_id: int) -> User:
    session = SessionLocal()
    return session.query(User).filter(User.telegram_id == telegram_id).first()


def get_in_queue(telegram_id: int, queue_id: int) -> PersonsInQueue:
    session = SessionLocal()
    db_person_in_queue = PersonsInQueue(
        user_id=telegram_id, queue_id=queue_id, enter_date=datetime.now()
    )
    session.add(db_person_in_queue)
    session.commit()
    session.refresh(db_person_in_queue)
    return db_person_in_queue


def drop_from_queue(telegram_id: int, queue_id: int):
    session = SessionLocal()
    session.query(PersonsInQueue).filter(
        PersonsInQueue.user_id == telegram_id,
        PersonsInQueue.queue_id == queue_id).delete()
