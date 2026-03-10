# Api de sistemas de reservas restaurant
from dataclasses import field
from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel
import asyncio
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm    
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI (
    title="API de sistemas de reservas restaurant",
    description="API EXAMEN 2"
    version="1.0.0"
)

Reserva = 

secret_key = "clave secreta"
Algoritmo = "HS256"
Acceso_token_expiracion_minutos = 30

class usuario(BaseModel):
    id: int = field(...,gt=0)
    nombre: str = field(...,min_length=6, max_length=50)


@app.get("/")
async def Restarurante():
    return{
        "Bienvenido al sitema de reservas de restaurant"
    }

@app.get("/bienvenido")
async def Restarurante():
   
        await asyncio.sleep(5)  
        return{  
         "mensaje": "Bienvenido al sistema de reservas"
         
        "estatus" : "200"
    }

@app.get("/V1/reservas/")
async def listar_reserva ():
     return{
       "total": len(reservas),
       "reservas": reservas
     }





@app.post("/reservas/")
