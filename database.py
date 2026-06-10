from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
  bind=engine, 
  class_=AsyncSession, 
  expire_on_commit=False
  )


class Base(DeclarativeBase):
  pass


async def get_db():
  async with AsyncSessionLocal() as db:
    yield db

