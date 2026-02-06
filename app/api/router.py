from fastapi import APIRouter
from app.api.endpoints import (
    files,
    users
)

router = APIRouter()

router.include_router(users.router)
router.include_router(files.router)
