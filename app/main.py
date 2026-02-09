from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="File Sharing Application", version="1.0.0")

app.include_router(router, prefix="/api/v1")


