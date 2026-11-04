from pydantic import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    llm_api_key: str=""
    chroma_path: str="chroma_db"
    chunk_size: int=1000
    chunk_overlap: int=150

    model_config=SettingsConfigDict(env_file=".env")

settings=Settings()