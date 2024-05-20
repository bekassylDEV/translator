from fastapi import APIRouter

from src.api.routes.v1 import router as api_v1_router

router = APIRouter()
router.include_router(api_v1_router)
