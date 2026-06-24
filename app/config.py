from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Personal Therapist"
    APP_SECRET_KEY: str
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    OPENAI_API_KEY: str
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3"
    GROQ_API_KEY: str = ""

    REDIS_URL: str = "redis://localhost:6379"
    HF_MODEL_SENTIMENT: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
