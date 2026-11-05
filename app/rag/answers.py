from pathlib import Path
from app.config import settings
from app.ingestion.store import search
from app.llm import chat

PROMPT_PATH=Path(__file__).parent.parent / "prompts" / "qa_system.txt"
SYSTEM_PROMPT=PROMPT_PATH.read_text(encoding="utf-8")

