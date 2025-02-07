# app/routers/home.py
from fastapi import APIRouter

router = APIRouter()

# router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/")
def home():
    return {"message": "Bienvenue sur l'API FastAPI !"}
