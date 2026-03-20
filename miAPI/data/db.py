from sqlachemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os 

#1. definir la URL de conexion
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
 )

engine= create_engine(DATABASE_URL)

session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )
Base= declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()