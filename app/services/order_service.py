import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.product import Product
from app.models.order import Order

async def process_checkout(
    db: AsyncSession, 
    redis: aioredis.Redis, 
    user_id: int, 
    product_id: int, 
    quantity: int
) -> Order:
    lock_key = f"lock:product:{product_id}"
    
    # Menggunakan Distributed Lock Redis (Timeout 5 detik)
    # Hanya 1 request yang bisa masuk ke blok ini dalam 1 milidetik
    async with redis.lock(lock_key, timeout=5, blocking_timeout=2):
        # 1. Ambil data stok terbaru langsung dari DB
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produk tidak ditemukan")

        # 2. Validasi Ketersediaan Stok
        if product.stock < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Stok tidak mencukupi. Stok tersisa: {product.stock}"
            )

        # 3. Potong Stok & Simpan Order
        product.stock -= quantity
        new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity, status="SUCCESS")
        
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        # 4. Invalidate Cache Produk di Redis karena stok telah berubah
        await redis.delete(f"cache:product:{product_id}")
        
        return new_order