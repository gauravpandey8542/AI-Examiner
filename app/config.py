from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-120b"
    top_k: int = 4
    llm_api_key: str=""
    chroma_path: str="chroma_db"
    chunk_size: int=1000
    chunk_overlap: int=150

    model_config=SettingsConfigDict(env_file=".env")

settings=Settings()