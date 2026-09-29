from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+pysqlite:///./info_manager.db"

engine = create_engine(
  DATABASE_URL,
  echo=True,
  connect_args={"check_same_thread": False}

)

SessoinLocal = sessionmaker(
  bind=engine,
  autoflush=False,
  autocommit=False
)