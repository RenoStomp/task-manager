from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .models import StatusEnum

# создаём базу объектам валидации и преобразования
class TaskBase(BaseModel):
    title: str = Field(..., min_Length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[StatusEnum] = StatusEnum.new

# сама задача наследуется от базы
class TaskCreate(TaskBase):
    pass

# схема для обновления задачи, где все поля необязательны к заполнению
# так же пустые поля обрезаются
class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[StatusEnum]

# схема для ответа пользователю
class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True     #разрешаем читать напрямую из бд
