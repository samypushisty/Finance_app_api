from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware
from api import router as api_router
from api.api_v1.services.base_schemas.schemas import StandartException
from core.config import settings
from core.models import db_helper

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    title="Trading App",
    docs_url=None, redoc_url=None
)

@main_app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=main_app.openapi_url,
        title=main_app.title + " - Swagger UI",
        oauth2_redirect_url=main_app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@main_app.get(main_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

main_app.include_router(
    api_router
)

origins = [
    "*"
    # "http://localhost:5173",
    # "http://127.0.0.1:5173",
]

@main_app.exception_handler(StandartException)
async def unicorn_exception_handler(request: Request, exc: StandartException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:main_app",
#         reload=True,
#         host=settings.run.host,
#         port=settings.run.port
#     )