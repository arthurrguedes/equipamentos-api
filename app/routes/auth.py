from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.security import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    novo = User(
        email=user.email,
        senha=hash_senha(user.senha)
    )
    db.add(novo)
    db.commit()
    return {"message": "Usuário criado"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verificar_senha(user.senha, db_user.senha):
        return {"erro": "Credenciais inválidas"}

    token = criar_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }