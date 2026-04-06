from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from database import get_db
from models import ProductoDB, Usuario, Categoria
from schemas.product_schema import Producto, ProductoResponse
import shutil

router = APIRouter(prefix="/productos", tags=["Productos"])


# 🛒 OBTENER PRODUCTOS
@router.get("/", response_model=list[ProductoResponse])
def obtener_productos(
    categoria_id: int = None,
    search: str = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(ProductoDB)

    if categoria_id:
        query = query.filter(ProductoDB.categoria_id == categoria_id)

    if search:
        query = query.filter(ProductoDB.nombre.ilike(f"%{search}%"))

    query = query.offset(offset).limit(limit)

    return query.all()


# ➕ AGREGAR PRODUCTO
@router.post("/", response_model=ProductoResponse)
def agregar_producto(
    nombre: str = Form(...),
    precio: int = Form(...),
    cantidad: int = Form(...),
    categoria_id: int = Form(...),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # validar usuario (simulado)
    user_db = db.query(Usuario).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # validar categoría
    categoria = db.query(Categoria).filter(
        Categoria.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no existe")

    # guardar imagen
    filename = None
    if imagen:
        filename = imagen.filename
        file_path = f"images/{filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)

    # crear producto
    nuevo = ProductoDB(
        nombre=nombre,
        precio=precio,
        cantidad=cantidad,
        categoria_id=categoria_id,
        usuario_id=user_db.id,
        imagen=filename
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ✏️ ACTUALIZAR PRODUCTO
@router.put("/{id}", response_model=ProductoResponse)
def actualizar_producto(
    id: int,
    producto_actualizado: Producto,
    db: Session = Depends(get_db)
):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.nombre = producto_actualizado.nombre
    producto.precio = producto_actualizado.precio
    producto.cantidad = producto_actualizado.cantidad
    producto.categoria_id = producto_actualizado.categoria_id

    db.commit()
    db.refresh(producto)

    return producto


# ❌ ELIMINAR PRODUCTO
@router.delete("/{id}")
def eliminar_producto(
    id: int,
    db: Session = Depends(get_db)
):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return {"mensaje": "Producto eliminado correctamente"}