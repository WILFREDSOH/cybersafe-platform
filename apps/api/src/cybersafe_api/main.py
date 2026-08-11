from fastapi import FastAPI

from cybersafe_api.api.v1.router import router as api_router

app = FastAPI(
    title="CyberSafe API",
    description="API backend for the CyberSafe cybersecurity platform.",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return the current API health status."""
    return {
        "status": "ok",
        "service": "cybersafe-api",
    }
