
# IMPORTACIONES

from fastapi import FastAPI, HTTPException
import asyncio
from typing import Optional

# INSTANCIA DEL SERVIDOR

app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)


# BASE DE DATOS FICTICIA

usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]


# ENDPOINTS GET


@app.get("/")
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}


@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
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


# Leer todos los usuarios
@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }


# POST - CREAR USUARIO

@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuarios(usuario: dict):

    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario creado",
        "Datos nuevos": usuario
    }


# PUT - ACTUALIZAR COMPLETO

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado completamente",
                "usuario": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# PATCH - ACTUALIZAR PARCIAL

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


# DELETE - ELIMINAR USUARIO

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado",
                "id": id
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
