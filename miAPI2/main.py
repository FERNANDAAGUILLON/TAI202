from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="API Biblioteca")


# MODELOS

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr


class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(default="disponible")

    class Config:
        schema_extra = {
            "example": {
                "nombre": "La timidez del dragón",
                "autor": "Jorge Bucay",
                "año": 1943,
                "paginas": 96
            }
        }


class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario
    fecha_prestamo: datetime = Field(default_factory=datetime.now)


# BASE DE DATOS TEMPORAL

libros: List[dict] = []
prestamos: List[dict] = []


# ENDPOINTS

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )

    libros.append(libro.dict())
    return libro


@app.get("/libros", response_model=List[Libro])
def listar_libros():
    return libros


@app.get("/libros/{nombre}", response_model=Libro)
def buscar_libro(nombre: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):
    for libro in libros:
        if libro["nombre"].lower() == prestamo.nombre_libro.lower():

            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return prestamo

    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.get("/prestamos", response_model=List[Prestamo])
def listar_prestamos():
    return prestamos


@app.put("/prestamos/{nombre_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(nombre_libro: str):
    for prestamo in prestamos:
        if prestamo["nombre_libro"].lower() == nombre_libro.lower():

            prestamos.remove(prestamo)

            for libro in libros:
                if libro["nombre"].lower() == nombre_libro.lower():
                    libro["estado"] = "disponible"
                    return {"detalle": "Libro devuelto"}

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo ya no existe"
    )


@app.delete("/prestamos/{nombre_libro}")
def eliminar_prestamo(nombre_libro: str):
    for prestamo in prestamos:
        if prestamo["nombre_libro"].lower() == nombre_libro.lower():
            prestamos.remove(prestamo)
            return {"detalle": "Préstamo eliminado"}

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo ya no existe"
    )