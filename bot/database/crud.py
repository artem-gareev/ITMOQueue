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


def create_practice(name: str, subject_id: int) -> PracticeTeacher:
    with SessionLocal() as session:
        db_practise = PracticeTeacher(
            name=name,
            subject_id=subject_id
        )
        session.add(db_practise)
        session.commit()
        session.refresh(db_practise)
        return db_practise


def get_all_subjects():
    with SessionLocal() as session:
        return session.query(Subject).all()


def get_all_users():
    with SessionLocal() as session:
        return session.query(User).all()


def get_persons_for_practice(practice_id: int) -> list[Queue]:
    with SessionLocal() as session:
        return session.query(Queue).filter(Queue.practice_id == practice_id,
                                           Queue.is_left == False).order_by(Queue.priority,
                                                                            Queue.num_in_order).all()


def get_person_for_practice(practice_id, person_id) -> Queue:
    with SessionLocal() as session:
        return session.query(Queue).filter(Queue.practice_id == practice_id,
                                           Queue.user_id == person_id).first()


def get_person_for_practice_by_id(practice_queue_id) -> Queue:
    with SessionLocal() as session:
        return session.query(Queue).filter(Queue.id == practice_queue_id).first()


def get_user_priority(user_id, practice_id):
    with SessionLocal() as session:
        last_left = session.query(Queue).filter(Queue.practice_id == practice_id,
                                                Queue.user_id == user_id,
                                                Queue.is_left).order_by(Queue.left_time.desc()).first()
        if last_left and last_left.left_time == datetime.now().date():
            return 1
        return 0


def get_persons_for_practice_with_priority(practice_id: int, priority: int) -> list[Queue]:
    with SessionLocal() as session:
        return session.query(Queue).filter(Queue.practice_id == practice_id,
                                           Queue.priority == priority,
                                           Queue.is_left == False).order_by(
            Queue.num_in_order).all()


def get_user(telegram_id: int) -> User:
    with SessionLocal() as session:
        return session.query(User).filter(User.telegram_id == telegram_id).first()


def enter_queue(user_id, practice_id, priority, number_to_enter) -> Queue:
    with SessionLocal() as session:
        db_person_for_practice = Queue(
            user_id=user_id,
            practice_id=practice_id,
            priority=priority,
            num_in_order=number_to_enter
        )
        session.add(db_person_for_practice)
        session.commit()
        session.refresh(db_person_for_practice)
        return db_person_for_practice


def drop_from_queue(telegram_id: int, practice_id: int):
    with SessionLocal() as session:
        session.query(Queue).filter_by(
            user_id=telegram_id,
            practice_id=practice_id).update({"is_left": True, "left_time": datetime.today()})
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


def delete_subject(subject_id: int):
    with SessionLocal() as session:
        session.query(Subject).filter(Subject.id == subject_id).delete()
        session.commit()


def delete_practice(practice_id: int):
    with SessionLocal() as session:
        session.query(PracticeTeacher).filter(PracticeTeacher.id == practice_id).delete()
        session.commit()


def edit_user_order_place(user_id: int, practice_id: int, order_place: int):
    with SessionLocal() as session:
        session.query(Queue).filter_by(
            user_id=user_id,
            practice_id=practice_id).update({"num_in_order": order_place})
        session.commit()


def move_queue(practice_id: int, priority: int, move_from: int, value):
    with SessionLocal() as session:
        session.query(Queue).filter(
            Queue.practice_id == practice_id,
            Queue.priority == priority,
            Queue.is_left == False,
            Queue.num_in_order > move_from).update({"num_in_order": Queue.num_in_order + value})
        session.commit()


def delete_person_by_in_queue_id(person_id: int):
    with SessionLocal() as session:
        session.query(Queue).filter(Queue.id == person_id).delete()
        session.commit()


def edit_user_priority(person_id, priority):
    with SessionLocal() as session:
        session.query(Queue).filter_by(
            id=person_id).update({"priority": priority})
        session.commit()
