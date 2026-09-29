from sqlalchemy.orm import Session
from sqlalchemy import select
from ..shemas import ComponentCreate, ComponentsUpdate
from ..models.components import Component

def get_components(session: Session):
  stmt = select(Component)
  return list(session.scalars(stmt).all())

def get_component_by_id(components_id:int, session:Session):
  component = select(Component).where(Component.id == components_id)
  return session.scalars( component).first()


def create_component(session:Session, payload:ComponentCreate):
  component = Component(**payload.model_dump())

  session.add(component)
  session.commit()
  session.refresh(component)

  return component

def component_by_id_update(session:Session, component_id:int, payload: ComponentsUpdate):

  stmt = select(Component).where(Component.id == component_id)

  item_by_id = session.scalars(stmt).first()

  if item_by_id is None:
    return None

  new_data = payload.model_dump(exclude_unset=True)

  for key,values in new_data.items():
    setattr(item_by_id,key,values)

  session.commit()
  session.refresh(item_by_id)

  return item_by_id

  
def del_component_by_id(session:Session,component_id:int):
  stmt= select(Component).where(Component.id == component_id)
  component = session.scalars(stmt).first()

  if component is None:
    return None

  session.delete(component)
  session.commit()
  return component



