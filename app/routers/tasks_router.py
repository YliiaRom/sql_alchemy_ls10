from fastapi import APIRouter, status,Request,Form
from fastapi.responses import RedirectResponse
from ..dependencies import SessionDep
from ..services.tasks import  get_tasks_by_session,create_task,update_task,get_task_by_id,delete_task

from ..shemas import TaskResponse, TaskCreate,TaskUpdate
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/tasks", tags=['tasks'])
template = Jinja2Templates(directory="templates")

@router.get("/")
def get_all_tasks(request:Request, db:SessionDep):
  tasks = get_tasks_by_session(db)

  return template.TemplateResponse(
    request=request,
    name="notes_page.html",
    context={
      "main_title":"Notes",
      "tasks":tasks
    }

  )



@router.post("/", response_model= TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(db:SessionDep, title:str = Form(...), description:str= Form(...)):
  new_task = TaskCreate(title=title,description=description)
 
  
  create_task(db, new_task)
  return RedirectResponse("/tasks/", status_code=303)


@router.patch('/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task_by_id(db: SessionDep,task_id:int, payload:TaskUpdate):
  return update_task(db, task_id, payload)


@router.get("/{task_id}/edit", status_code=status.HTTP_200_OK)
def edit_task_page(request:Request,db:SessionDep, task_id: int):

  task = get_task_by_id(db,task_id)
  
  return template.TemplateResponse(
    request=request,
    name="update_task_page.html",
    context={
      "main_title":"update",
      "task":task
    }
  )

@router.post("/{task_id}/edit")
def update_old_task(db:SessionDep, task_id: int, title:str = Form(...), description:str = Form(...)):


  modify_task = TaskUpdate(title=title, description=description)
  update_task(db, task_id, modify_task)
  return RedirectResponse("/tasks/", status_code=303)

@router.post("/{task_id}/delete")
def delete_task_by_id(db:SessionDep, task_id:int):
  delete_task(db, task_id)
  return RedirectResponse('/tasks/', status_code=303)