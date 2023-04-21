from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from pydantic.types import List

from src.database import get_async_session
from src.operations.models import operation

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


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    print(query)
    result = await session.execute(query)

    return [dict(r._mapping) for r in result]
