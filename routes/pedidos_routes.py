from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

pedidos = []  # 🔥 memoria simple (suficiente por ahora)

@router.post("/")
def crear_pedido(data: dict):
    pedidos.append(data)
    return {"message": "Pedido guardado correctamente"}

@router.get("/")
def obtener_pedidos():
    return pedidos