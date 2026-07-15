import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from auth import create_access_token

from auth import hash_password
from config import settings
from main import app
from database import get_db, Base
from models import User, Post

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


test_engine = create_async_engine(settings.test_database_url)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():

  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  yield

  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)



@pytest_asyncio.fixture
async def db_session():

  connection = await test_engine.connect()
  transaction = await connection.begin()
  session = AsyncSession(bind=connection)

  yield session

  await session.close()
  await transaction.rollback()
  await connection.close()


@pytest_asyncio.fixture
async def client(db_session):

  async def override_get_db():
    yield db_session

  app.dependency_overrides[get_db] = override_get_db

  transport = ASGITransport(app=app)

  async with AsyncClient(
    transport=transport, 
    base_url="http://test"
    ) as client:

    yield client

  app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):

  new_user = User(
    username="opeyemi",
    email="opeyemi@gmail.com",
    passwordhash=hash_password("101010")
  )

  db_session.add(new_user)
  await db_session.commit()
  await db_session.refresh(new_user)

  return new_user

@pytest_asyncio.fixture
async def test_post(test_user, db_session):

  user_id = test_user.id

  new_post = Post(
    user_id=user_id,
    title="Test post",
    content="This is testing post"
  )

  db_session.add(new_post)
  await db_session.commit()
  await db_session.refresh(new_post, attribute_names=["to_user"])

  return new_post

@pytest_asyncio.fixture
async def auth_header(test_user):

  token = create_access_token({
    "sub": str(test_user.id)
  })

  return {
    "Authorization": f"Bearer {token}"
  }

  


  



