from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Membuat async engine untuk PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Membuat sessionmaker untuk operasi async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# Dependency untuk mendapatkan database session di API endpoint
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()