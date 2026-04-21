from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.equipamento import Equipamento
from app.models.user import User
from app.schemas.equipamento import EquipamentoCreate, EquipamentoResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/equipamentos", tags=["Equipamentos"])

# Conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Busca usuário logado
def get_usuario_logado(db: Session, email: str):
    usuario = db.query(User).filter(User.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario

# Criar equipamento
@router.post("/", response_model=EquipamentoResponse)
def criar_equipamento(
    dados: EquipamentoCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    usuario = get_usuario_logado(db, user)

    novo = Equipamento(
        nome=dados.nome,
        status=dados.status,
        user_id=usuario.id
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

# Listar equipamentos do usuário
@router.get("/", response_model=list[EquipamentoResponse])
def listar_equipamentos(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    usuario = get_usuario_logado(db, user)

    equipamentos = db.query(Equipamento).filter(
        Equipamento.user_id == usuario.id
    ).all()

    return equipamentos

# GET por ID (somente do usuário logado)
@router.get("/{id}", response_model=EquipamentoResponse)
def buscar_equipamento(
    id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    usuario = get_usuario_logado(db, user)

    equipamento = db.query(Equipamento).filter(
        Equipamento.id == id,
        Equipamento.user_id == usuario.id
    ).first()

    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")

    return equipamento

# Atualizar (somente do usuário logado)
@router.put("/{id}", response_model=EquipamentoResponse)
def atualizar_equipamento(
    id: int,
    dados: EquipamentoCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    usuario = get_usuario_logado(db, user)

    equipamento = db.query(Equipamento).filter(
        Equipamento.id == id,
        Equipamento.user_id == usuario.id
    ).first()

    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")

    equipamento.nome = dados.nome
    equipamento.status = dados.status

    db.commit()
    db.refresh(equipamento)

    return equipamento

# Deletar (somente do usuário logado)
@router.delete("/{id}")
def deletar_equipamento(
    id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    usuario = get_usuario_logado(db, user)

    equipamento = db.query(Equipamento).filter(
        Equipamento.id == id,
        Equipamento.user_id == usuario.id
    ).first()

    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")

    db.delete(equipamento)
    db.commit()

    return {"message": "Equipamento deletado com sucesso"}