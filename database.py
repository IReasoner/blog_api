from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMEY_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(SQLALCHEMEY_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
  bind=engine, 
  class_=AsyncSession, 
  expire_on_commit=False
  )


class Base(DeclarativeBase):
  pass


# Ai CODE DONT REALLY UNDERSTAND AND WORKED FOR SYNC AND ASYNC ALSO
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# ENDS HERE

async def get_db():
  async with AsyncSessionLocal() as db:
    yield db

