from fastapi import HTTPException, status, Depends, APIRouter, UploadFile
from typing import Annotated

from database import get_db
from models import User, Post
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.concurrency import run_in_threadpool
from io import BytesIO
from config import settings
from PIL import UnidentifiedImageError


from schemas import PostResponse, UserCreate, UserPublicResponse, UserPrivateResponse, UpdateUser, Token
from auth import hash_password, verify_password, create_access_token, currentUser
from fastapi.security import OAuth2PasswordRequestForm
from image_utils import delete_profile_image, image_processing

 

router = APIRouter()

@router.get("/me", response_model=UserPrivateResponse)
def get_me(current_user: currentUser):
  return current_user


@router.post("/login", response_model=Token)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(User).where(func.lower(User.email) == form_data.username.lower()))
  user = result.scalar_one_or_none()

  if user is None or not verify_password(plain_password=form_data.password, hashed_password=user.passwordhash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Invalid Credentials"
      )
  
  data = {
    "sub": str(user.id)
  }

  access_token = create_access_token(data)

  return {
    "access_token": access_token
  }

  
# CREATE USER
@router.post("/register", response_model=UserPrivateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):

  results = await db.execute(select(User).where(func.lower(User.username) == user.username.lower()))
  existing_user = results.scalars().first()

  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exist")
  

  email = await db.execute(select(User).where(func.lower(User.email) == user.email.lower()))
  existing_email = email.scalars().first()

  if existing_email:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

  hashed_password = hash_password(password=user.password)

  new_user = User(
    username=user.username, 
    email=user.email.lower(), 
    passwordhash=hashed_password
    )
  
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user, attribute_names=["to_post"])

  return new_user

# UPDATE EXISTING USERS
@router.patch("/{user_id}", response_model=UserPrivateResponse)
async def update_user(
  user_id: int,
  current_user: currentUser, 
  data: UpdateUser, 
  db: Annotated[AsyncSession, Depends(get_db)]
  ):


  if current_user.id != user_id:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, 
          detail="Not authorized to update this user"
          )
  
  if data.username:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is not None:
      if user.username.lower() != current_user.username.lower():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exist")
      

  if data.email:
    result = await db.execute(select(User).where(User.id == user_id)) 
    user = result.scalars().first()

    if user is not None:
      if user.email.lower() != current_user.email.lower():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exist")

 
  data_list = data.model_dump(exclude_unset=True)

  for key, value in data_list.items():
    setattr(current_user, key, value)

  await db.commit()
  await db.refresh(current_user, attribute_names=["to_post"])

  return current_user

# DELETE EXISTING USER
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: currentUser, db: Annotated[AsyncSession, Depends(get_db)]):

  if current_user.id != user_id:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, 
          detail="Not authorized to delete this user"
          )
  
  old_filename = current_user.image_file
  
  await db.delete(current_user)
  await db.commit()

  if old_filename:
    delete_profile_image(old_filename)


# GET USERS ALL POST
@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_post(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()

  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
  
  all_get = await db.execute(select(Post).options(selectinload(Post.to_user)).where(Post.user_id == user_id))
  all_post = all_get.scalars().all()

  return all_post


# GET USERS DETAILS 
@router.get("/{user_id}", response_model=UserPublicResponse)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()

  if user:
    return user
  
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


# UPDATING PROFILE IMAGE

@router.patch("/{user_id}/picture", response_model=UserPrivateResponse)
async def update_user_profile(
  user_id: int,
  current_user: currentUser,
  image: UploadFile,
  db: Annotated[AsyncSession, Depends(get_db)]
  ):


  if current_user.id != user_id:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, 
          detail="Not authorized to update this users image"
          )
  
  
  content = await image.read()

  if len(content) > settings.max_profile_image_size:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"image should not execeed {settings.max_profile_image_size // 1024 // 1024}MB"
    )
  

  try:
    filename = await run_in_threadpool(image_processing, content)
  except UnidentifiedImageError:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid image"
    )
  except Exception:
    raise


  old_filename = current_user.image_file  
  
  current_user.image_file = filename # type: ignore
  
  await db.commit()
  await db.refresh(current_user, attribute_names=["to_post"])

  delete_profile_image(old_filename)

  return current_user



# DELETING USER PROFILE

@router.delete("/{user_id}/picture", response_model=UserPrivateResponse)
async def delete_user_profile(
  user_id: int,
  current_user: currentUser,
  db: Annotated[AsyncSession, Depends(get_db)]
  ):


  if current_user.id != user_id:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, 
          detail="Not authorized to delete this users image"
          )

  old_filename = current_user.image_file  

  if old_filename is None:
    raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail="no profile image to delete"
          )
  

  current_user.image_file = None
  
  await db.commit()
  await db.refresh(current_user, attribute_names=["to_post"])

  delete_profile_image(old_filename)

  return current_user