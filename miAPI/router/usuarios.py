from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from data.db import usuarios
from models.usuario import Usuario
from security.auth import verificar_peticion

router = APIRouter(prefix="/v1", tags=["Usuarios"])

# ==============================
# PARAMETROS
# ==============================

@router.get("/parametroOb/{id}")
async def consultauno(id: int):
    return {
        "mensaje": "usuario encontrado",
        "usuario": id,
        "status": "200"
    }

@router.get("/parametroOp/")
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
# CRUD
# ==============================

@router.get("/usuarios/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@router.post("/usuarios/")
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

@router.put("/usuarios/{id}")
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

@router.patch("/usuarios/{id}")
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

@router.delete("/usuarios/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):

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