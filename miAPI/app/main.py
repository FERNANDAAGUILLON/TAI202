

# IMPORTACIONES

import secrets
from fastapi import FastAPI, HTTPException, Depends
import asyncio
from fastapi import status
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic,HTTPAuthorizationCredentials, HTTPBasicCredentials


# ==============================
# INSTANCIA DEL SERVIDOR
# ==============================

app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)


# ==============================
# BASE DE DATOS FICTICIA
# ==============================

usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]


# ==============================
# MODELO PYDANTIC (VALIDACIONES)
# ==============================

class Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

# seguridad 
security= HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credenciales.username,"MariaFernanda")
    contrasena_correcta= secrets.compare_digest(credenciales.password,"123456")
    
    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
            
        )
    return credenciales.username

# ==============================
# ENDPOINTS GET
# ==============================

@app.get("/")
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}


@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(2)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }


# Parámetro obligatorio
@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultauno(id: int):
    return {
        "mensaje": "usuario encontrado",
        "usuario": id,
        "status": "200"
    }


# Parámetro opcional
@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {
                    "mensaje": "usuario encontrado",
                    "usuario": usuarioK
                }
        return {"mensaje": "usuario no encontrado", "status": "200"}
    else:
        return {"mensaje": "No se proporciono id", "status": "200"}


# ==============================
# CRUD USUARIOS
# ==============================

# GET - Leer todos
@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }



# POST - Crear usuario
@app.post("/v1/usuarios/", tags=["HTTP CRUD"])
async def agregar_usuarios(usuario: Usuario):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario creado",
        "Datos nuevos": usuario
    }


# PUT - Actualizar completo
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario_actualizado: Usuario):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.dict()
            return {
                "mensaje": "Usuario actualizado completamente",
                "usuario": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# PATCH - Actualización parcial
@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_parcial(id: int, datos: dict):

    for usr in usuarios:
        if usr["id"] == id:
            usr.update(datos)
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# DELETE - Eliminar usuario
@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int,usuarioAuth: str = Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "id": id
            }
    
    raise HTTPException(
        status_code=401,
        detail="Usuario no encontrado"
    )

