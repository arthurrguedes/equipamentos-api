from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes import equipamentos

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(equipamentos.router)

@app.get("/")
def root():
    return {"message": "API rodando 🚀"}