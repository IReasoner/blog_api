from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  secret_key: str
  algorithms: str
  access_token_expire_minutes: int

  class Config:
    env_file = ".env"



settings = Settings() # type: ignore


