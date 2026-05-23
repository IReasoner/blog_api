from fastapi import HTTPException, status, Depends, APIRouter
from typing import Annotated

from database import get_db
from models import Post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import PostCreate, PostResponse, PostUpdate
from auth import currentUser


router = APIRouter()

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
  post: PostCreate, 
  current_user: currentUser,
  db: Annotated[AsyncSession, Depends(get_db)]
  ):

  new_post = Post(
    user_id=current_user.id, 
    title=post.title, 
    content=post.content
    )

  db.add(new_post)
  await db.commit()
  await db.refresh(new_post, attribute_names=["to_user"])

  return new_post 

# UPDATE POST
@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
  post_id: int, post_update: PostUpdate, 
  current_user: currentUser,
  db: Annotated[AsyncSession, Depends(get_db)]
  ):

  result = await db.execute(select(Post).where(Post.id == post_id))
  post = result.scalar_one_or_none()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  

  if current_user.id != post.user_id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN, 
      detail="Not authorized to edit this post"
      )

  data_list = post_update.model_dump(exclude_unset=True)

  for key, value in data_list.items():
    setattr(post, key, value)

  await db.commit()
  await db.refresh(post, attribute_names=["to_user"])

  return post

# DELETE POST 
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
  post_id: int, 
  current_user: currentUser,
  db: Annotated[AsyncSession, Depends(get_db)]
  ):

  result = await db.execute(select(Post).where(Post.id == post_id))
  post = result.scalar_one_or_none()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  if current_user.id != post.user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to delete this post"
        )
  
  await db.delete(post)
  await db.commit()

  

  
@router.get("", response_model=list[PostResponse]) 
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(Post).order_by(Post.date_posted.desc()))
  posts = result.scalars().all()

  return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(Post).where(Post.id == post_id).order_by(Post.date_posted.desc()))
  post = result.scalars().first()
  
  if post:
    return post
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found",)
