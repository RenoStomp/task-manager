from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
from .database import Base

# класс для определения статуса задачи
class StatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

# класс самой задачи
class Task(Base):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True, nullable=False)

    description = Column(String, nullable=False)

    due_date = Column(DateTime, nullable=False)

    status = Column(Enum(StatusEnum), default=StatusEnum.new, nullable=False)
