from fastapi import APIRouter

from cybersafe_api.api.v1.analysis import router as analysis_router

router = APIRouter(prefix="/api/v1")

router.include_router(analysis_router)
