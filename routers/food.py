from typing import List
from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response
from repositories.food_repository import FoodRepository
from schemas.food import (
    FoodCreate, FoodUpdate, FoodPartialUpdate, FoodResponse,
    FoodSearchParams, PaginationParams, PaginatedResponse,
    ApiResponse, ApiListResponse, PaginationInfo
)
from dependencies import get_food_repository
import math

router = APIRouter(prefix="/v1/foods", tags=["foods"])


@router.get("/search", response_model=ApiListResponse[FoodResponse])
async def search_foods(
    food_name: str = Query(None, description="식품이름 (부분 일치 검색)"),
    research_year: str = Query(None, pattern=r'^\d{4}$', description="연도(YYYY)"),
    maker_name: str = Query(None, description="지역/제조사"),
    food_code: str = Query(None, description="식품코드"),
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    식품 정보를 검색 조건에 따라 조회합니다.
    """
    search_params = FoodSearchParams(
        food_name=food_name,
        research_year=research_year,
        maker_name=maker_name,
        food_code=food_code
    )
    
    foods = await food_repo.search(search_params)
    food_responses = [FoodResponse.model_validate(food) for food in foods]
    
    return ApiListResponse[FoodResponse](
        data=food_responses,
        count=len(food_responses)
    )


@router.get("", response_model=PaginatedResponse[FoodResponse])
async def get_foods(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    모든 식품 목록을 페이지네이션과 함께 조회합니다.
    """
    pagination_params = PaginationParams(page=page, limit=limit)
    foods, total = await food_repo.get_all(pagination_params)
    
    food_responses = [FoodResponse.model_validate(food) for food in foods]
    total_pages = math.ceil(total / limit)
    
    pagination_info = PaginationInfo(
        page=page,
        limit=limit,
        total=total,
        totalPages=total_pages
    )
    
    return PaginatedResponse[FoodResponse](
        data=food_responses,
        pagination=pagination_info
    )


@router.get("/{food_id}", response_model=ApiResponse[FoodResponse])
async def get_food(
    food_id: int,
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    특정 식품 정보를 조회합니다.
    """
    food = await food_repo.get_by_id(food_id)
    food_response = FoodResponse.model_validate(food)
    
    return ApiResponse[FoodResponse](data=food_response)


@router.post("", response_model=ApiResponse[FoodResponse], status_code=status.HTTP_201_CREATED)
async def create_food(
    food_data: FoodCreate,
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    새로운 식품 정보를 등록합니다.
    """
    food = await food_repo.create(food_data)
    food_response = FoodResponse.model_validate(food)
    
    return ApiResponse[FoodResponse](data=food_response)


@router.put("/{food_id}", response_model=ApiResponse[FoodResponse])
async def update_food(
    food_id: int,
    food_data: FoodUpdate,
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    특정 식품의 전체 정보를 수정합니다.
    """
    food = await food_repo.update(food_id, food_data)
    food_response = FoodResponse.model_validate(food)
    
    return ApiResponse[FoodResponse](data=food_response)


@router.patch("/{food_id}", response_model=ApiResponse[FoodResponse])
async def partial_update_food(
    food_id: int,
    food_data: FoodPartialUpdate,
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    특정 식품의 일부 정보를 수정합니다.
    """
    food = await food_repo.partial_update(food_id, food_data)
    food_response = FoodResponse.model_validate(food)
    
    return ApiResponse[FoodResponse](data=food_response)


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food(
    food_id: int,
    food_repo: FoodRepository = Depends(get_food_repository)
):
    """
    특정 식품 정보를 삭제합니다.
    """
    await food_repo.delete(food_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)