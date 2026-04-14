from pydantic import BaseModel

class EquipamentoCreate(BaseModel):
    nome: str
    status: str | None = "Disponível"

class EquipamentoResponse(BaseModel):
    id: int
    nome: str
    status: str

    class Config:
        from_attributes = True