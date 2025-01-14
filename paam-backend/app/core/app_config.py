from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    app_name: str = "PAAM"
    openai_api_key: str
    openai_model: str
    tavily_api_key: str
    postgres_db_uri: str
    
    class Config:
        env_file = ".env"
    
settings = Settings()