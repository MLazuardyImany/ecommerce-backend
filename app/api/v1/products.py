import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as aioredis

from app.core.database import get_db
from app.api.deps import get_redis
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db)
):
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    cache_key = f"cache:product:{product_id}"
    
    # 1. Cek Caching di Redis
    cached_product = await redis.get(cache_key)
    if cached_product:
        return json.loads(cached_product)
    
    # 2. Jika tidak ada di Redis (Cache Miss), Query ke PostgreSQL
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    # 3. Simpan hasil query ke Redis (TTL 60 detik)
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "created_at": product.created_at.isoformat()
    }
    await redis.set(cache_key, json.dumps(product_data), ex=60)
    
    return product

@router.get("/", response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()