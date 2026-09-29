from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.components import Task
from ..shemas import TaskCreate, TaskUpdate


def get_tasks_by_session(session:Session):
  stmt = select(Task)

  return list(session.scalars(stmt).all())

def create_task(session:Session, payload:TaskCreate):
  task = Task(**payload.model_dump())
  session.add(task)
  session.commit()
  session.refresh(task)
  return task

def get_task_by_id(session:Session, task_id:int):
  stmt = select(Task).where(Task.id == task_id)
  task = session.scalars(stmt).first()
  return task

def update_task(session:Session,task_id:int, payload:TaskUpdate):
  stmt = select(Task).where(Task.id == task_id)
  task = session.scalars(stmt).first()

  if task is None:
    return None

  data = payload.model_dump(exclude_unset=True)

  for key,value in data.items():
    setattr(task,key,value)

  session.commit()
  session.refresh(task)

  return task



def delete_task(session:Session, task_id:int):
  stmt = select(Task).where(Task.id == task_id)
  task=session.scalars(stmt).first()

  if task is None:
    return None

  session.delete(task)
  session.commit()
  return task


