from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    status = Column(String, default="Disponível")