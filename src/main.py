import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.api.errors.http_error import http_error_handler
from src.api.errors.validation_error import http422_error_handler
from src.api.routes.api import router as api_router
from src.core import settings
from src.core.events import create_start_app_handler, create_stop_app_handler
from src.core.logging import setup_default_logging

logger = logging.getLogger("queue")


def get_application() -> FastAPI:
    setup_default_logging(settings.DEBUG)

    application = FastAPI(**settings.fastapi_kwargs)

    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    application.add_event_handler("startup", create_start_app_handler())
    application.add_event_handler("shutdown", create_stop_app_handler())

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
