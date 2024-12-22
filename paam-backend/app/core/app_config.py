from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    app_name: str = "PAAM"
    
    class Config:
        env_file = ".env"
    
settings = Settings()