from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .models import StatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_Length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[StatusEnum] = StatusEnum.new

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[StatusEnum]

class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True