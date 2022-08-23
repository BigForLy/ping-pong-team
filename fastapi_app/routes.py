from fastapi import APIRouter
from app import app

router = APIRouter()
router.include_router(app.router)
