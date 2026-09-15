from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.core.database import get_db
from app.api.deps import get_redis
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import process_checkout

router = APIRouter()

@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def checkout(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    # Sementara kita perumpamakan user_id = 1 (Nanti bisa pakai JWT Auth)
    dummy_user_id = 1
    
    order = await process_checkout(
        db=db,
        redis=redis,
        user_id=dummy_user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity
    )
    return order