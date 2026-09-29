from fastapi import APIRouter, status, Request,Form
from fastapi.responses import RedirectResponse
from ..dependencies import SessionDep
from ..services.components_service import get_components,create_component, component_by_id_update,get_component_by_id,del_component_by_id
from ..shemas import ComponentCreate, ComponentsUpdate, ComponentsResponse,ColorChecker
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

import json

with open("data/components.json", "r", encoding="utf-8") as file:
  base_components = json.load(file)


router = APIRouter(prefix='/components', tags=["components"])

@router.get("/")
def get_all_components(request: Request, db: SessionDep):
  try:

    components = get_components(db)
    return templates.TemplateResponse(
      request=request,
      name="index.html",
      context={"main_title":"db: SessionDep", "base_components": base_components, "components": components}

    )
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="not content")


@router.get('/form')
def get_form(request:Request):
  return templates.TemplateResponse(
    request=request,
    name="component_form_page.html",
    context={"main_title":"Form"}

  )

@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_new_component(db:SessionDep, title:str=Form(...),description:str = Form(...), link:str=Form(...),color_checker:ColorChecker=Form(...)):
  new_component = ComponentCreate(title=title,description=description,link=link,color_checker=color_checker)
  try:
   create_component(db, new_component)
   return RedirectResponse('/components/', status_code=303)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.patch("/{component_id}", response_model=ComponentsResponse, status_code=status.HTTP_200_OK)
def component_update(db:SessionDep,component_id:int, payload: ComponentsUpdate):
  component = get_component_by_id(component_id,db)
  if component is None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="NO_CONTENT")
  try:
   return component_by_id_update(db,component_id,payload)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="409_CONFLICT")

@router.post("/{component_id}/delete")
def delete_component(db:SessionDep, component_id:int):
  del_component_by_id(db,component_id)

  return RedirectResponse("/components/", status_code=303)
