import jwt
import pytest
from config import settings
from fastapi import HTTPException
from datetime import datetime, UTC, timedelta
from auth import (
  hash_password, verify_password, 
  create_access_token, verify_token, 
  get_current_user
  )

def test_hash_password():

  password = "101010"

  hashed_password = hash_password(password)

  assert hashed_password != password
  assert isinstance(hashed_password, str)


def test_verify_password():

  password = "101010"

  hashed_password = hash_password(password)
  assert verify_password(password, hashed_password)


def test_not_verify_password():

  password = "101010"

  hashed_password = hash_password(password)
  assert not verify_password("wrong", hashed_password)



def test_create_access_token():

  payload = {
    "sub": "1"
  }

  token = create_access_token(payload)

  decoded = jwt.decode(
    token,
    settings.secret_key,
    algorithms=[settings.algorithms]
  )

  assert isinstance(token, str)
  assert decoded["sub"] == "1"
  assert "exp" in decoded



def test_verify_token_valid():

  payload = {
    "sub": "2"
  }

  token = create_access_token(payload)

  user_id = verify_token(token)

  assert user_id == "2"


def test_verify_token_is_none():

  user_id = verify_token("abdefjdfkj")

  assert user_id is None

def test_expired_verify_token():

  expired_payload = {
    "sub": 1,
    "exp": datetime.now(UTC) - timedelta(minutes=1)
  }

  expired_token = jwt.encode(
    expired_payload,
    settings.secret_key,
    algorithm=settings.algorithms
  )

  assert verify_token(expired_token) is None

@pytest.mark.asyncio
async def test_get_current_user_valid(test_user, db_session):

  token = create_access_token({
    "sub": str(test_user.id)
  })

  user = await get_current_user(
    token=token,
    db=db_session
  )


  assert user.id == test_user.id #type:ignore
  assert user.email == test_user.email #type:ignore


@pytest.mark.asyncio
async def test_get_current_user_invalid_or_expire(db_session):

  with pytest.raises(HTTPException) as exc:

    await get_current_user(
      token="hdajhdgad",
      db=db_session
    )

  assert exc.value.status_code == 401
  assert exc.value.detail == "Invalid or expired token"

@pytest.mark.asyncio
async def test_get_current_user_is_none(db_session):

  token = create_access_token({
    "sub": str(2)
  })

  with pytest.raises(HTTPException) as exc:

    await get_current_user(
      token=token,
      db=db_session
    )

  assert exc.value.status_code == 401
  assert exc.value.detail == "Invalid or expired token"


  

