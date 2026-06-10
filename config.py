from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  secret_key: str
  algorithms: str
  access_token_expire_minutes: int
  reset_token_expire_minutes: int
  max_profile_image_size: int = 5 * 1024 * 1025
  email_address: str
  email_password: str
  email_host: str
  email_port: int
  frontend_url: str
  database_url: str


  class Config:
    env_file = ".env"



settings = Settings() # type: ignore


