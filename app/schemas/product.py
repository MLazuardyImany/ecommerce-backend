from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, example="Laptop Gaming RTX 4060")
    description: Optional[str] = Field(None, example="Laptop gaming spesifikasi tinggi")
    price: float = Field(..., gt=0, example=15000000.0)
    stock: int = Field(..., ge=0, example=10)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True