from pydantic_settings import BaseSettings, SettingsConfigDict

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
  test_database_url: str

  aws_access_key_id: str
  aws_secret_access_key: str
  aws_region_name: str
  aws_bucket_name: str


  model_config = SettingsConfigDict(
    env_file=".env"
  )



settings = Settings() # type: ignore


