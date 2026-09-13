from fastapi import FastAPI

app = FastAPI(
    title="AI Research Agent",
    description="Autonomous AI research agent",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}