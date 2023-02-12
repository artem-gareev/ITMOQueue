from datetime import datetime

from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, Integer, Boolean

from database.database import Base


class IdMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)


class Subject(Base, IdMixin):
    __tablename__ = "subjects"

    name = Column(VARCHAR)


class PracticeTeacher(Base, IdMixin):
    __tablename__ = "practice_teachers"

    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE'))
    name = Column(VARCHAR)


class PersonInQueue(Base, IdMixin):
    __tablename__ = "queue"

    practice_id = Column(Integer, ForeignKey("practice_teachers.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.telegram_id", ondelete='CASCADE'))

    is_new = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    num_in_order = Column(Integer, default=1)

    enter_time = Column(TIMESTAMP, default=datetime.utcnow())
    left_time = Column(TIMESTAMP)
