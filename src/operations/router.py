import time

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

class Operation(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    type: str

    class Config:
        orm_mode: True

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get('/long_operation')
@cache(expire=30)
def get_long_operation():
    time.sleep(2)
    return "Many many data"


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    print(query)
    result = await session.execute(query)

    return [dict(r._mapping) for r in result]

@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": 200}
