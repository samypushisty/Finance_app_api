import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api import router as api_router
from core.config import settings
app = FastAPI(
    title="Trading App"
)

app.include_router(
    api_router,
    prefix=settings.api.prefix
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port
    )