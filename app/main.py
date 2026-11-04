from fastapi import FastAPI

app = FastAPI(title="AI Examiner")

@app.get("/health")
def health():
    return {"status": "ok"}