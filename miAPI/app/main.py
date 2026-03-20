from fastapi import FastAPI
from router import usuarios, misc

app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)

# Registrar routers
app.include_router(misc.router)
app.include_router(usuarios.router)
