from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

# связываем со всеми необходимыми файлами
from . import models, schemas, crud, database, auth

# создаём таблицы в базе, если их ещё нет
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Task Manager API")

# открываем сессию для связи с бд, которая потом закрывается
def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

# создаём новую задачу
@app.post(
    "/tasks",
    response_model=schemas.TaskOut,
    dependencies=[Depends(auth.get_token_header)]
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

# получить список задач
@app.get(
    "/tasks",
    response_model=List[schemas.TaskOut],
    dependencies=[Depends(auth.get_token_header)]
)
def read_tasks(status: Optional[models.StatusEnum] = None,
               due_date: Optional[datetime] = None,
               db: Session = Depends(get_db)):
    return crud.get_tasks(db, status, due_date)

# получить только одну задачу по ID
@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(auth.get_token_header)]
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task: raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# обновить задачу
@app.patch(
    "/tasks/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(auth.get_token_header)]
)
def update_task(
        task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, db_task, updates)

# удалить задачу
@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.get_token_header)]
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task: raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, db_task)
