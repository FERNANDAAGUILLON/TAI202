from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def obtener_usuarios(db: Session = Depends(get_db)):

    # Se agregó la conexión a la base de datos y se consulta directamente 
    # la tabla de usuarios en lugar de usar listas locales

    usuarios = db.query(dbUsuario).all()

    # Se devuelve el total de registros junto con los datos obtenidos
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }


@router.get("/{id}")
async def obtener_usuario(id: int, db: Session = Depends(get_db)):

    # Se agregó este endpoint para obtener un usuario por su ID desde la BD

    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    # Se valida que el usuario exista
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "usuario": usuario,
        "status": "200"
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(usuario: crear_usuario, db: Session = Depends(get_db)):

    # Se crea un nuevo usuario con los datos recibidos

    nuevo = dbUsuario(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

     #Se guarda el nuevo registro en la base de datos
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Usuario creado",
        "usuario": nuevo
    }


@router.put("/{id}")
async def actualizar_usuario(id: int, usuario: crear_usuario, db: Session = Depends(get_db)):

    #Se busca el usuario en la BD para actualizar todos sus datos

    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    # Se valida que exista el registro
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Se reemplazan completamente los datos del usuario
    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario actualizado",
        "usuario": usuario_db
    }


@router.patch("/{id}")
async def actualizar_parcial(id: int, datos: dict, db: Session = Depends(get_db)):

    # Se agregó PATCH para actualizar solo algunos campos del usuario

    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    # Validación de existencia
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Solo se modifican los campos enviados en la petición
    if "nombre" in datos:
        usuario_db.nombre = datos["nombre"]

    if "edad" in datos:
        usuario_db.edad = datos["edad"]

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario actualizado parcialmente",
        "usuario": usuario_db
    }


@router.delete("/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db), usuarioAuth: str = Depends(verificar_peticion)):

    # Se agregó validación con autenticación y eliminación desde la BD

    usuario_db = db.query(dbUsuario).filter(dbUsuario.id == id).first()

    # Se verifica que el usuario exista
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Se elimina el registro y se guardan los cambios
    db.delete(usuario_db)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "status": "200"
    }