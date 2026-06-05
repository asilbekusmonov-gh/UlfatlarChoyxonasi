from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Using a local SQLite file with the async driver
DATABASE_URL = "sqlite+aiosqlite:///ulfatlar.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory for handling transactions
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Base class for all DB models
class Base(DeclarativeBase):
    pass

# Helper function to auto-create tables on startup
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)