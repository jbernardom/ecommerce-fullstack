from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Categoria
from schemas.categoria_schema import CategoriaCreate
from auth import verificar_admin

router = APIRouter(prefix="/categorias", tags=["Categorias"])


# 🔥 CREAR CATEGORÍA (SOLO ADMIN)
@router.post("/")
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    admin=Depends(verificar_admin)
):
    existente = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe"
        )

    nueva = Categoria(nombre=categoria.nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# 🔥 LISTAR CATEGORÍAS
@router.get("/")
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()
