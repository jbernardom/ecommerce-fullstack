from pydantic import BaseModel, Field


class Producto(BaseModel):
    nombre: str = Field(..., min_length=2)
    precio: int = Field(..., gt=0)
    cantidad: int = Field(..., ge=0)
    categoria_id: int


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: int
    cantidad: int
    categoria_id: int
    imagen: str | None = None

    class Config:
        from_attributes = True