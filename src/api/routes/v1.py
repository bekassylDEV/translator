# Standard Imports
from fastapi import APIRouter

# App Imports
from src.api.routes import translation

router = APIRouter(prefix="/v1")
router.include_router(translation.router, prefix="/translation")
