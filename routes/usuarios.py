from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from pydantic import BaseModel
from auth import crear_token, encriptar_password, verificar_password

router = APIRouter()


# 🔹 MODELO
class UsuarioCreate(BaseModel):
    username: str
    password: str


# 👤 CREAR USUARIO
@router.post("/usuarios")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo = Usuario(
        username=usuario.username,
        password=encriptar_password(usuario.password),
        role="admin"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"mensaje": "Usuario creado"}


# 🔐 LOGIN
@router.post("/login")
def login(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verificar_password(usuario.password, user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = crear_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "mensaje": "Login exitoso",
        "access_token": token,
        "token_type": "bearer"
    }