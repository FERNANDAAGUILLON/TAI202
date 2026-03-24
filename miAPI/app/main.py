from fastapi import FastAPI
from app.router import usuario, misc
from app.data.db import engine
from app.data import usuario as usuarioDB

usuarioDB.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Mi primer API",
    description="Maria Fernanda BA",
    version="1.0"
)

# Registrar routers
app.include_router(misc.misc)
app.include_router(usuario.router)
