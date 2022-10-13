from datetime import datetime
from typing import Optional

from database.database import SessionLocal
from database.models import Queue, Subject, User, PracticeTeacher


def create_user(telegram_id: int, username: Optional[str]) -> User:
    with SessionLocal() as session:
        db_user = User(
            telegram_id=telegram_id, name=username,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def create_subject(name: str) -> Subject:
    with SessionLocal() as session:
        db_subject = Subject(
            name=name,
        )
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return db_subject


def get_all_subjects():
    with SessionLocal() as session:
        return session.query(Subject).all()


def get_persons_for_practice(practice_id: int) -> list[Queue]:
    with SessionLocal() as session:
        return session.query(Queue).filter(Queue.practice_id == practice_id).order_by(
            Queue.priority, Queue.num_in_order).all()


def get_user(telegram_id: int) -> User:
    with SessionLocal() as session:
        return session.query(User).filter(User.telegram_id == telegram_id).first()


# def get_in_queue(telegram_id: int, practice_id: int) -> Queue:
#     with SessionLocal() as session:
#         db_person_for_practice = Queue(
#             user_id=telegram_id, practice_id=practice_id, enter_date=datetime.now()
#         )
#         session.add(db_person_for_practice)
#         session.commit()
#         session.refresh(db_person_for_practice)
#         return db_person_for_practice


def drop_from_queue(telegram_id: int, practice_id: int):
    with SessionLocal() as session:
        session.query(Queue).filter_by(
            user_id=telegram_id,
            practice_id=practice_id).update({"is_left": True})
        session.commit()


def get_practice(practice_id: int) -> PracticeTeacher:
    with SessionLocal() as session:
        return session.query(PracticeTeacher).filter(PracticeTeacher.id == practice_id).first()


def get_subject(subject_id: int) -> Subject:
    with SessionLocal() as session:
        return session.query(Subject).filter(Subject.id == subject_id).first()


def get_all_practices_for_subject(subject_id: int) -> list[Subject]:
    with SessionLocal() as session:
        return session.query(PracticeTeacher).filter(PracticeTeacher.subject_id == subject_id).all()
