from fastapi import APIRouter
import asyncio

router = APIRouter()

@router.get("/")
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@router.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(2)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }