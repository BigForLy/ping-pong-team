from fastapi import APIRouter
from app import app as app2

router = APIRouter()
router.include_router(app2.router)
