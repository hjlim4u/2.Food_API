from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repositories.food_repository import FoodRepository


async def get_food_repository(db: AsyncSession = Depends(get_db)) -> FoodRepository:
    """식품 리포지토리 의존성 주입"""
    return FoodRepository(db)