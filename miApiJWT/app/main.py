# ===============================
# IMPORTACIONES
# ===============================

from fastapi import FastAPI, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

# Seguridad
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# ===============================
# CONFIGURACION FASTAPI
# ===============================

app = FastAPI(
    title="Mi primer API",
    description="API con OAuth2 y JWT",
    version="1.0"
)

# ===============================
# BASE DE DATOS FICTICIA
# ===============================

usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21, "password": "123"},
    {"id": 2, "nombre": "Aly", "edad": 21, "password": "123"},
    {"id": 3, "nombre": "Dulce", "edad": 21, "password": "123"},
]

# ===============================
# CONFIGURACION JWT
# ===============================

SECRET_KEY = "clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ===============================
# MODELO USUARIO
# ===============================

class Usuario(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=1, le=123)

# ===============================
# CREAR TOKEN
# ===============================

def crear_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ===============================
# VALIDAR TOKEN
# ===============================

def verificar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return usuario

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

# ===============================
# LOGIN - GENERAR TOKEN
# ===============================

@app.post("/token")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    for usuario in usuarios:

        if (
            usuario["nombre"] == form_data.username
            and usuario["password"] == form_data.password
        ):

            token = crear_token({
                "sub": usuario["nombre"]
            })

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(
        status_code=401,
        detail="Credenciales incorrectas"
    )

# ===============================
# ENDPOINTS BASICOS
# ===============================

@app.get("/")

async def holamundo():

    return {
        "mensaje": "Hola Mundo FastAPI"
    }


@app.get("/bienvenido")

async def bienvenido():

    await asyncio.sleep(2)

    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }

# ===============================
# CRUD USUARIOS
# ===============================

@app.get("/v1/usuarios/")

async def leer_usuarios():

    return {
        "total": len(usuarios),
        "usuarios": usuarios
    }


@app.post("/v1/usuarios/")

async def agregar_usuario(usuario: Usuario):

    for usr in usuarios:

        if usr["id"] == usuario.id:

            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario creado",
        "usuario": usuario
    }

# ===============================
# PUT PROTEGIDO
# ===============================

@app.put("/v1/usuarios/{id}")

async def actualizar_usuario(
    id: int,
    usuario_actualizado: Usuario,
    token: str = Depends(oauth2_scheme)
):

    usuario_token = verificar_token(token)

    for index, usr in enumerate(usuarios):

        if usr["id"] == id:

            usuarios[index]["id"] = usuario_actualizado.id
            usuarios[index]["nombre"] = usuario_actualizado.nombre
            usuarios[index]["edad"] = usuario_actualizado.edad

            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuarios[index],
                "actualizado_por": usuario_token
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# ===============================
# DELETE PROTEGIDO
# ===============================

@app.delete("/v1/usuarios/{id}")

async def eliminar_usuario(
    id: int,
    token: str = Depends(oauth2_scheme)
):

    usuario_token = verificar_token(token)

    for index, usr in enumerate(usuarios):

        if usr["id"] == id:

            usuarios.pop(index)

            return {
                "mensaje": "Usuario eliminado",
                "id": id,
                "eliminado_por": usuario_token
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )