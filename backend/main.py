from fastapi import FastAPI
from backend.config import settings

app = FastAPI(
    title="Policy-to-Code Mapper API",
    description="Context-aware IDE backend for real-time security policy guidance.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "policy-to-code-mapper"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
