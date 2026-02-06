from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="File Sharing APP")

app.include_router(router, prefix="/api/v1")
