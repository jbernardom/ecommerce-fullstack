from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario

SECRET_KEY = "secret"
ALGORITHM = "HS256"

# 🔥 CAMBIO CLAVE (YA NO OAuth2)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(Usuario).filter(
            Usuario.username == username
        ).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def verificar_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo administradores"
        )
    return current_user