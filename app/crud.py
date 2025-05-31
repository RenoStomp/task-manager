from pyexpat import model
from sqlalchemy.orm import Session
from . import models, schemas

# получить задачу по ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# получить список задач отфильтрованных либо по статусу, либо по дате
def get_tasks(db: Session, status=None, due_date=None):
    q = db.query(models.Task)
    if status:
        q = q.filter(models.Task.status == status)
    if due_date:
        q = q.filter(models.Task.due_date == due_date)
    return q.all()

# создать новую задачу
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model.dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# обновляем задачу
def update_task(db: Session, db_task: models.Task, updates: schemas.TaskUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# удаляем задачу
def delete_task(db: Session, db_task: models.Task):
    db.delete(db_task)
    db.commit()
