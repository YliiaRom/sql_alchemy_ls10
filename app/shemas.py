from pydantic import BaseModel,Field,ConfigDict
from enum import Enum
from datetime import datetime

class TaskBase(BaseModel):
   
      title: str
      description: str

class TaskCreate(TaskBase):
      pass

class TaskUpdate(BaseModel):
      title: str | None = Field(default=None, max_length=500)
      description: str | None = None

class TaskResponse(TaskBase):
      id:int
      model_config = ConfigDict(from_attributes=True)
      

class ColorChecker(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

class ComponentBase(BaseModel):
  title:str =Field(max_length=500, examples=["title"])
  description: str
  link:str 
  color_checker:ColorChecker

class ComponentCreate(ComponentBase):
      pass 
class ComponentsUpdate(BaseModel):
  title:str|  None =Field(default=None, max_length=500)
  description: str | None = None
  link:str | None = None
  color_checker:ColorChecker | None = None


class ComponentsResponse(ComponentBase):
    id : int
    created_at: datetime

    model_config= ConfigDict(from_attributes=True)

