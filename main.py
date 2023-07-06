# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # import psycopg2
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker
# # from sqlalchemy import Column, Integer, String, Boolean
# # from sqlalchemy.ext.declarative import declarative_base

# # app = FastAPI()

# # class Taskmodw(BaseModel):
# #     id: int
# #     title: str
# #     description: str
# #     completed: bool


# # Base = declarative_base()

# # class Task(Base):
# #     __tablename__ = "tasks"

# #     id = Column(Integer, primary_key=True)
# #     title = Column(String)
# #     description = Column(String)
# #     completed = Column(Boolean)



# # db_url = "postgresql+psycopg2://postgres:ct##123456@localhost/mydb"
# # engine = create_engine(db_url)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # db = SessionLocal()


# # app = FastAPI()

# # @app.get("/tasks/{task_id}")
# # def get_task(task_id: int):
# #     task = db.query(Task).filter(Task.id == task_id).first()
# #     if task is None:
# #         return {"message": "Task not found"}
# #     return task

# # @app.post("/tasks")
# # def create_task(task: Task):
# #     db.add(task)
# #     db.commit()
# #     db.refresh(task)
# #     return task

# # @app.put("/tasks/{task_id}")
# # def update_task(task_id: int, task: Task):
# #     db_task = db.query(Task).filter(Task.id == task_id).first()
# #     if db_task is None:
# #         return {"message": "Task not found"}
# #     db_task.title = task.title
# #     db_task.description = task.description
# #     db_task.completed = task.completed
# #     db.commit()
# #     db.refresh(db_task)
# #     return db_task

# # @app.delete("/tasks/{task_id}")
# # def delete_task(task_id: int):
# #     db_task = db.query(Task).filter(Task.id == task_id).first()
# #     if db_task is None:
# #         return {"message": "Task not found"}
# #     db.delete(db_task)
# #     db.commit()
# #     return {"message": "Task deleted"}


# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy import create_engine, Column, Integer, String, Boolean
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# app = FastAPI()

# # Define Pydantic model for Task
# class Task(BaseModel):
#     id: int
#     title: str
#     description: str
#     completed: bool
    
#     class Config:
#         orm_mode = True

# # Define SQLAlchemy model
# Base = declarative_base()

# class TaskDB(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     description = Column(String)
#     completed = Column(Boolean)

# # Database connection setup
# db_url = "postgresql+psycopg2://postgres:ct##123456@localhost/mydb"
# engine = create_engine(db_url)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
# Base.metadata.create_all(bind=engine)


# # Routes
# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task(task_id: int):
#     task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if task is None:
#         return {"message": "Task not found"}
#     return task

# # @app.post("/tasks", response_model=Task)
# # def create_task(task: Task):
# #     db_task = TaskDB(**task.dict())
# #     db.add(db_task)
# #     db.commit()
# #     db.refresh(db_task)
# #     return db_task

# @app.post('/task/', response_model = Task, status_code=201)
# def create_task(task: Task):
#    new_task = Task(
#         task_name = task.task_name,
#         task_des = task.task_des,
#         created_by =task.created_by,
#         datecreated = task.date_created,
#    )
#    db.add(new_task)
#    db.commit()
#    return new_task


# @app.put("/tasks/{task_id}", response_model=Task)
# def update_task(task_id: int, task: Task):
#     db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if db_task is None:
#         return {"message": "Task not found"}
#     db_task.title = task.title
#     db_task.description = task.description
#     db_task.completed = task.completed
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if db_task is None:
#         return {"message": "Task not found"}
#     db.delete(db_task)
#     db.commit()
#     return {"message": "Task deleted"}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from model import Task
from schema import task_schema
from session import create_get_session

app = FastAPI()


@app.get("/task", response_model=List[task_schema], status_code=200)
async def read_tasks(db: Session = Depends(create_get_session)):
   tasks = db.query(Task).all()
   return tasks

@app.post('/task', response_model = task_schema, status_code=201)
async def create_task(task: task_schema, db: Session = Depends(create_get_session)):
   new_task = Task(
        task_name = task.task_name,
        task_des = task.task_des,
        created_by =task.created_by,
   )
   db.add(new_task)
   db.commit()

   return new_task

@app.get("/task/{id}", response_model = task_schema, status_code=200)
async def get_task(id:int,db: Session = Depends(create_get_session)):
   task = db.query(Task).get(id)
   return task

@app.patch("/task/{id}", response_model = task_schema, status_code=200)
async def update_task(id:int, task:task_schema, db: Session = Depends(create_get_session)):
   db_task = db.query(Task).get(id)
   db_task.task_name = task.task_name
   db_task.task_des =  task.task_des
   db.commit()
   db.refresh(db_task)

   return db_task

@app.delete('/task/{id}', status_code=200)
async def delete_task(id:int, db: Session = Depends(create_get_session)):
   db_task = db.query(Task).get(id)
   if not db_task:
       raise HTTPException(status_code="404",detail="Task id does not exist")
 
   db.delete(db_task)
   db.commit()

   return None
