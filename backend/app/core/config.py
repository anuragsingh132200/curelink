from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Disha AI Health Coach"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = "postgresql://curelink:curelink_password@localhost:5432/curelink_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # LLM Configuration
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "gemini"  # "gemini" or "openai"
    LLM_MODEL: str = "gemini-2.5-flash"  # Latest Gemini Flash model
    MAX_CONTEXT_TOKENS: int = 8000
    MAX_RESPONSE_TOKENS: int = 1000

    # Chat Configuration
    MESSAGES_PER_PAGE: int = 20
    MAX_CONVERSATION_HISTORY: int = 50
    TYPING_INDICATOR_DELAY: float = 0.5

    # Memory Configuration
    MEMORY_IMPORTANCE_THRESHOLD: float = 0.7
    MAX_MEMORIES_IN_CONTEXT: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
