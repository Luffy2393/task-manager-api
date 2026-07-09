from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session  
from fastapi.security import OAuth2PasswordRequestForm

from database import engine, get_db
import models
import schemas
import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")

def read_root():
    return {"message": "This is My First Api Call!"} 

@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_task = models.Task(\
        title=task.title, 
        description=task.description,
        owner_id=current_user.id
        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=list[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=schemas.Token)
def login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == from_data.username).first()
    if not user or not auth.verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}