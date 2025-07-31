from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.exc import IntegrityError
from models.food import Food
from schemas.food import FoodCreate, FoodUpdate, FoodPartialUpdate, FoodSearchParams, PaginationParams
from exceptions import FoodNotFoundError, FoodAlreadyExistsError, DatabaseError


class FoodRepository:
    """식품 데이터 접근 레이어"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, food_data: FoodCreate) -> Food:
        """새로운 식품을 생성합니다."""
        try:
            db_food = Food(**food_data.model_dump())
            self.db.add(db_food)
            await self.db.flush()
            await self.db.refresh(db_food)
            return db_food
        except IntegrityError:
            await self.db.rollback()
            raise FoodAlreadyExistsError(food_data.food_cd)
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"식품 생성 중 오류가 발생했습니다: {str(e)}")

    async def get_by_id(self, food_id: int) -> Food:
        """ID로 식품을 조회합니다."""
        try:
            result = await self.db.execute(select(Food).where(Food.id == food_id))
            food = result.scalar_one_or_none()
            if not food:
                raise FoodNotFoundError(food_id=food_id)
            return food
        except FoodNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"식품 조회 중 오류가 발생했습니다: {str(e)}")

    async def get_by_food_cd(self, food_cd: str) -> Optional[Food]:
        """식품코드로 식품을 조회합니다."""
        try:
            result = await self.db.execute(select(Food).where(Food.food_cd == food_cd))
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseError(f"식품 조회 중 오류가 발생했습니다: {str(e)}")

    async def get_all(self, pagination: PaginationParams) -> tuple[List[Food], int]:
        """모든 식품을 페이지네이션과 함께 조회합니다."""
        try:
            # 전체 개수 조회
            count_result = await self.db.execute(select(func.count(Food.id)))
            total = count_result.scalar()

            # 페이지네이션된 데이터 조회
            offset = (pagination.page - 1) * pagination.limit
            result = await self.db.execute(
                select(Food)
                .offset(offset)
                .limit(pagination.limit)
                .order_by(Food.id)
            )
            foods = result.scalars().all()
            
            return list(foods), total
        except Exception as e:
            raise DatabaseError(f"식품 목록 조회 중 오류가 발생했습니다: {str(e)}")

    async def search(self, search_params: FoodSearchParams) -> List[Food]:
        """검색 조건에 따라 식품을 조회합니다."""
        try:
            query = select(Food)
            conditions = []

            if search_params.food_name:
                conditions.append(Food.food_name.contains(search_params.food_name))
            
            if search_params.research_year:
                conditions.append(Food.research_year == search_params.research_year)
            
            if search_params.maker_name:
                conditions.append(Food.maker_name.contains(search_params.maker_name))
            
            if search_params.food_code:
                conditions.append(Food.food_cd.contains(search_params.food_code))

            if conditions:
                query = query.where(and_(*conditions))

            query = query.order_by(Food.id)
            result = await self.db.execute(query)
            return list(result.scalars().all())
            
        except Exception as e:
            raise DatabaseError(f"식품 검색 중 오류가 발생했습니다: {str(e)}")

    async def update(self, food_id: int, food_data: FoodUpdate) -> Food:
        """식품 정보를 전체 수정합니다."""
        try:
            food = await self.get_by_id(food_id)
            
            # 식품코드 중복 확인 (다른 식품이 같은 코드를 사용하는지)
            if food_data.food_cd != food.food_cd:
                existing_food = await self.get_by_food_cd(food_data.food_cd)
                if existing_food and existing_food.id != food_id:
                    raise FoodAlreadyExistsError(food_data.food_cd)

            # 모든 필드 업데이트
            for field, value in food_data.model_dump().items():
                setattr(food, field, value)

            await self.db.flush()
            await self.db.refresh(food)
            return food
            
        except (FoodNotFoundError, FoodAlreadyExistsError):
            raise
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"식품 수정 중 오류가 발생했습니다: {str(e)}")

    async def partial_update(self, food_id: int, food_data: FoodPartialUpdate) -> Food:
        """식품 정보를 부분 수정합니다."""
        try:
            food = await self.get_by_id(food_id)
            
            # 수정할 데이터만 추출 (None이 아닌 값들만)
            update_data = food_data.model_dump(exclude_unset=True)
            
            # 식품코드 중복 확인
            if 'food_cd' in update_data and update_data['food_cd'] != food.food_cd:
                existing_food = await self.get_by_food_cd(update_data['food_cd'])
                if existing_food and existing_food.id != food_id:
                    raise FoodAlreadyExistsError(update_data['food_cd'])

            # 지정된 필드만 업데이트
            for field, value in update_data.items():
                setattr(food, field, value)

            await self.db.flush()
            await self.db.refresh(food)
            return food
            
        except (FoodNotFoundError, FoodAlreadyExistsError):
            raise
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"식품 부분 수정 중 오류가 발생했습니다: {str(e)}")

    async def delete(self, food_id: int) -> None:
        """식품을 삭제합니다."""
        try:
            food = await self.get_by_id(food_id)
            await self.db.delete(food)
            await self.db.flush()
            
        except FoodNotFoundError:
            raise
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"식품 삭제 중 오류가 발생했습니다: {str(e)}")