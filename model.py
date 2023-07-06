from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text,Boolean
from database import Base

class Task(Base):
   __tablename__ = "Tasks"
   id = Column(Integer, primary_key=True, index=True)
   task_name = Column(String(20))
   task_des = Column(Text())
   created_by = Column(String(20))
#    completed: Column(Boolean)