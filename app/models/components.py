from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column
from ..shemas import ColorChecker

from sqlalchemy import String, Text,Integer, Enum,func
from enum import Enum as pyEnum
import datetime

class Base(DeclarativeBase):
  pass


class Component(Base):
  __tablename__="component"


  id:Mapped[int]= mapped_column(Integer,primary_key=True)
  title:Mapped[str]=mapped_column(String(500),server_default='не ввели значення')
  description:Mapped[str]=mapped_column(Text)
  link:Mapped[str]=mapped_column()
  color_checker:Mapped[ColorChecker] = mapped_column(Enum(ColorChecker))
  created_at:Mapped[datetime.datetime] = mapped_column(
      server_default=func.now()
  )
class Task(Base):
    __tablename__="tasks"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(500))
    description:Mapped[str| None]= mapped_column(String(1000))