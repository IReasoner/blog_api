from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime



# TOKEN SCHEMAS

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"

  model_config = ConfigDict(from_attributes=True)


# USER SCHEMAS
class UserCreate(BaseModel):
  username: str = Field(..., min_length=1)
  email: EmailStr = Field(..., min_length=1)
  password: str = Field(..., min_length=5)
  

class UpdateUser(BaseModel):
  username: str | None = Field(default=None, min_length=1)
  email: EmailStr | None = Field(default=None, min_length=1)

class UserPublicResponse(BaseModel):
  id: int
  username: str
  image_file: str | None
  image_url: str

  model_config = ConfigDict(from_attributes=True)

class UserPrivateResponse(UserPublicResponse):
  email: EmailStr


# POST SCHEMAS 
class PostCreate(BaseModel):
  title: str 
  content: str 


class PostUpdate(BaseModel):
  title: str | None = Field(default=None, min_length=1)
  content: str | None = Field(default=None, min_length=1)
  # user_id: int | None # TEMPORARY 


class PostResponse(BaseModel):
  id: int 
  to_user: UserPublicResponse
  user_id: int
  title: str 
  content: str 
  date_posted: datetime


  model_config = ConfigDict(from_attributes=True)

  

  