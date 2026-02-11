
from fastapi import FastAPI, Query
from pydantic import BaseModel
import asyncio


# INSTANCIA DEL SERVIDOR

app = FastAPI()


# MODELO PARA BODY

class Usuario(BaseModel):
    nombre: str
    correo: str



# ENDPOINT 1: BÁSICO

@app.get("/")
async def holamundo():
    return {
        "mensaje": "Hola Mundo FastAPI"
    }


# ==========================
# ENDPOINT 2: CON ESPERA
# ==========================
@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a mi API con FastAPI",
        "estatus": 200
    }


# ==========================
# ENDPOINT 3: PARÁMETRO EN RUTA (OBLIGATORIO)
# ==========================
@app.get("/usuario/{id}")
async def obtener_usuario(id: int):
    return {
        "mensaje": "Usuario encontrado",
        "id": id
    }


# ==========================
# ENDPOINT 4: PARÁMETRO QUERY OPCIONAL
# ==========================
@app.get("/productos")
async def productos(categoria: str = None):
    return {
        "mensaje": "Lista de productos",
        "categoria": categoria
    }


# ==========================
# ENDPOINT 5: PARÁMETRO QUERY OBLIGATORIO
# ==========================
@app.get("/buscar")
async def buscar(nombre: str = Query(...)):
    return {
        "mensaje": f"Buscando {nombre}"
    }


# ==========================
# ENDPOINT 6: PARÁMETROS EN BODY (POST)
# ==========================
@app.post("/crear-usuario")
async def crear_usuario(usuario: Usuario):
    return {
        "mensaje": "Usuario creado correctamente",
        "datos": usuario
    }

        