from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, Integer

from database.database import Base


class IdMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)


class Queue(Base, IdMixin):
    __tablename__ = "queues"

    name = Column(VARCHAR)


class PersonsInQueue(Base, IdMixin):
    __tablename__ = "persons_in_queue"

    queue_id = Column(Integer, ForeignKey("queues.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.telegram_id", ondelete='CASCADE'))
    enter_date = Column(TIMESTAMP)
