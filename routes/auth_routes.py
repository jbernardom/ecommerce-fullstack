from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas.user_schema import UserCreate, UserLogin
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🔥 REGISTRO (USUARIO NORMAL)
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(
        Usuario.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_password = hash_password(user.password)

    nuevo_usuario = Usuario(
        username=user.username,
        password=hashed_password,
        role="user"  # 🔥 AHORA ES USUARIO NORMAL
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"message": "Usuario creado correctamente"}


# 🔐 LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(
        Usuario.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔥 HACER ADMIN (ENDPOINT NUEVO)
@router.post("/make-admin/{username}")
def make_admin(username: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        Usuario.username == username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.role = "admin"
    db.commit()

    return {"message": f"{username} ahora es admin"}