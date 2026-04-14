from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.equipamento import Equipamento
from app.schemas.equipamento import EquipamentoCreate, EquipamentoResponse

router = APIRouter(prefix="/equipamentos", tags=["Equipamentos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EquipamentoResponse)
def criar_equipamento(dados: EquipamentoCreate, db: Session = Depends(get_db)):
    novo = Equipamento(nome=dados.nome, status=dados.status)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[EquipamentoResponse])
def listar_equipamentos(db: Session = Depends(get_db)):
    return db.query(Equipamento).all()

@router.put("/{id}", response_model=EquipamentoResponse)
def atualizar_equipamento(id: int, dados: EquipamentoCreate, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.id == id).first()

    if not equipamento:
        return {"erro": "Equipamento não encontrado"}

    equipamento.nome = dados.nome
    equipamento.status = dados.status

    db.commit()
    db.refresh(equipamento)
    return equipamento

@router.delete("/{id}")
def deletar_equipamento(id: int, db: Session = Depends(get_db)):
    equipamento = db.query(Equipamento).filter(Equipamento.id == id).first()

    if not equipamento:
        return {"erro": "Equipamento não encontrado"}

    db.delete(equipamento)
    db.commit()

    return {"message": "Equipamento deletado"}