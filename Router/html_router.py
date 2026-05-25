from fastapi import Request, HTTPException, status, Depends, APIRouter
from typing import Annotated

from fastapi.templating import Jinja2Templates

from database import get_db
from models import User, Post
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import PostResponse
  
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/login", include_in_schema=False)
def load_login_page(request: Request):
  return templates.TemplateResponse(
    request, 
    "login_page.html", 
    {
      "title": "Login page", 
      "dont_show_div": True
      })


@router.get("/register", include_in_schema=False)
def load_register_page(request: Request):
  return templates.TemplateResponse(
    request, 
    "register_page.html", 
    {
      "title": "Register page", 
      "dont_show_div": True
      })

@router.get("/account", include_in_schema=False)
def load_account_page(request: Request):
  return templates.TemplateResponse(
    request, 
    "account_page.html", 
    {
      "title": "account page", 
      })


@router.get("/", include_in_schema=False, response_model=PostResponse)
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(Post).options(selectinload(Post.to_user)).order_by(Post.date_posted.desc()))
  posts = result.scalars().all()

  return templates.TemplateResponse(
    request, 
    "main_post_page.html", 
    {
      "posts": posts, 
      "title": "Home"
     })


@router.get("/post/{post_id}", include_in_schema=False)
async def post_page(post_id: int, request: Request, db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(Post).options(selectinload(Post.to_user)).where(Post.id == post_id))
  post = result.scalars().first()

  if post:
    return templates.TemplateResponse(
      request,
      "single_post_page.html", 
      {
        "c": post,
        "title": "Post"
        })
    
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# WE CAN GIVE A ROUTE NAME WHICH WILL REPRESENT A FUNCTION NAME
@router.get("/user/{user_id}/posts", include_in_schema=False, name="all_get")  
async def all_user_post_page(request: Request, user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):

  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()

  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
  
  thepost = await db.execute(
    select(Post).options(selectinload(Post.to_user))
    .where(Post.user_id == user_id).order_by(Post.date_posted.desc())
    )
  
  all_post = thepost.scalars().all()

  return templates.TemplateResponse(
    request, 
    "user_post_page.html", 
    {
      "posts": all_post, 
      "title": f"{user.username}'s posts"
      })

