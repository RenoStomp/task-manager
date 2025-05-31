from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from . import models, schemas, crud, database, auth

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Task Manager API")

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@app.post("/tasks", response_model=schemas.TaskOut,
          dependencies=[Depends(auth.get_token_header)])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(task, db)

@app.get("/tasks", response_model=List[schemas.TaskOut],
         dependencies=[Depends(auth.get_token_header)])
def read_tasks(status: Optional[models.StatusEnum] = None,
               due_date: Optional[datetime] = None,
               db: Session = Depends(get_db)):
    return crud.get_tasks(db, status, due_date)

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut,
         dependencies=[Depends(auth.get_token_header)])
def read_task(task_id: int, db: Session = Depends(get_db)):
    t = crud.get_task(db, task_id)
    if not t: raise HTTPException(status_code=404, detail="Task not found")
    return t

@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut,
           dependencies=[Depends(auth.get_token_header)])
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    t = crud.get_task(db, task_id)
    if not t: raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[Depends(auth.get_token_header)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    t = crud.get_task(db, task_id)
    if not t: raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, t)
