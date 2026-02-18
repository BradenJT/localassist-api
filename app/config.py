from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "LocalAssist API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    
    # JWT
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # DynamoDB
    LEADS_TABLE_NAME: str = "leads"
    USERS_TABLE_NAME: str = "users"
    AWS_REGION: str = "us-east-1"
    DYNAMODB_ENDPOINT: Optional[str] = "http://localhost:8000"
    
    # CORS - stored as string, converted to list via method
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Use model_config instead of Config class
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }
    
    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()