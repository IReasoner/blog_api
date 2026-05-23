from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  secret_key: str
  algorithms: str
  access_token_expire_minutes: int
  max_profile_image_size: int = 5 * 1024 * 1025

  class Config:
    env_file = ".env"



settings = Settings() # type: ignore


