from app.database import SessoinLocal

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

def get_session():
  session =  SessoinLocal()
  try:
    yield session
  finally:
    session.close()


SessionDep = Annotated[Session, Depends(get_session)]