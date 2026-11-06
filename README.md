The pipeline: upload PDF → chunk → embed → store in Chroma → retrieve → LLM answers with page citations.

Tech stack: FastAPI, Chroma, Groq gpt-oss-120b.

Setup steps: create the venv, pip install -r requirements.txt, copy .env.example to .env and add the key, run uvicorn app.main:app --reload.

A note that it refuses to answer when the document doesn’t contain the answer.