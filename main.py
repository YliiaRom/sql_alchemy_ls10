from contextlib import asynccontextmanager
from app.database import engine
from app.models.components import Base
from fastapi import FastAPI,Request
from app.routers.tasks_router import router as tasks
from app.routers.components_rourers import router as components
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

with open('data/components.json', "r", encoding="utf-8") as file:
  base_components = json.load(file)

@asynccontextmanager
async def lifespan(app:FastAPI):
  Base.metadata.create_all(bind=engine)
  yield



app = FastAPI(title="Romanenko Yuliia / SQLAlchemy components API", lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
app.mount(
  "/static/",
  StaticFiles(directory="static"),
  name="static",
)

app.include_router(tasks)
app.include_router(components)

@app.get('/')
def read_root(request:Request):
  return templates.TemplateResponse(
    request=request,
    name="home_page.html",
    context={'main_title':"data/components.json", "base_components": base_components}
  )
  
