import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from fastapi import HTTPException, Depends, status
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from database import get_db
from config import settings


# OAUTH2PASSWORDBEARER

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="/api/users/login"
)

# PASSWORD LOGIC
password_hash = PasswordHash.recommended()

def hash_password(password: str):
  return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return password_hash.verify(plain_password, hashed_password)

# AUTHENTICATION LOGIC

def create_access_token(data: dict):

  to_encode = data.copy()

  expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

  to_encode.update({
    "exp": expire_time
  })

  encoded_jwt = jwt.encode(
    to_encode,
    settings.secret_key,
    algorithm=settings.algorithms

  )

  return encoded_jwt

def verify_token(token: str):

  try:

    payload = jwt.decode(
      token,
      settings.secret_key,
      algorithms=[settings.algorithms]
    )

  except jwt.InvalidTokenError:
    return None
  else: 
    return payload.get("sub")
  


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Annotated[AsyncSession, Depends(get_db)]
    ): 

  user_id = verify_token(token)

  if user_id is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Invalid or expired token"
      )
  
  # try:
  #   user_id = int(user_id)
  # except(TypeError, ValueError):
  #   raise HTTPException(
  #     status_code=status.HTTP_401_UNAUTHORIZED, 
  #     detail="Invalid or expired token"
  #     )
  
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalar_one_or_none()

  return user


currentUser = Annotated[User, Depends(get_current_user)]
