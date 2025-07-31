from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Generic, TypeVar
import re

T = TypeVar('T')


class FoodBase(BaseModel):
    """식품 기본 스키마"""
    food_cd: str = Field(..., min_length=1, max_length=50, description="식품코드")
    group_name: str = Field(..., min_length=1, max_length=100, description="식품군명")
    food_name: str = Field(..., min_length=1, max_length=200, description="식품이름")
    research_year: str = Field(..., pattern=r'^\d{4}$', description="연도(YYYY)")
    maker_name: str = Field(..., min_length=1, max_length=100, description="지역/제조사")
    ref_name: str = Field(..., min_length=1, max_length=100, description="자료명")
    serving_size: str = Field(..., min_length=1, max_length=50, description="1회 제공량")
    calorie: float = Field(..., ge=0, description="칼로리(kcal)")
    carbohydrate: float = Field(..., ge=0, description="탄수화물(g)")
    protein: float = Field(..., ge=0, description="단백질(g)")
    province: float = Field(..., ge=0, description="지방(g)")
    sugars: float = Field(..., ge=0, description="총당류(g)")
    salt: float = Field(..., ge=0, description="나트륨(mg)")
    cholesterol: float = Field(..., ge=0, description="콜레스테롤(mg)")
    saturated_fatty_acids: float = Field(..., ge=0, description="포화지방산(g)")
    trans_fat: float = Field(..., ge=0, description="트랜스지방(g)")

    @field_validator('research_year')
    @classmethod
    def validate_year(cls, v):
        if not re.match(r'^\d{4}$', v):
            raise ValueError('연도는 YYYY 형식이어야 합니다')
        year = int(v)
        if year < 1900 or year > 2100:
            raise ValueError('연도는 1900년과 2100년 사이여야 합니다')
        return v


class FoodCreate(FoodBase):
    """식품 생성 스키마"""
    pass


class FoodUpdate(FoodBase):
    """식품 전체 수정 스키마"""
    pass


class FoodPartialUpdate(BaseModel):
    """식품 부분 수정 스키마"""
    food_cd: Optional[str] = Field(None, min_length=1, max_length=50)
    group_name: Optional[str] = Field(None, min_length=1, max_length=100)
    food_name: Optional[str] = Field(None, min_length=1, max_length=200)
    research_year: Optional[str] = Field(None, pattern=r'^\d{4}$')
    maker_name: Optional[str] = Field(None, min_length=1, max_length=100)
    ref_name: Optional[str] = Field(None, min_length=1, max_length=100)
    serving_size: Optional[str] = Field(None, min_length=1, max_length=50)
    calorie: Optional[float] = Field(None, ge=0)
    carbohydrate: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    province: Optional[float] = Field(None, ge=0)
    sugars: Optional[float] = Field(None, ge=0)
    salt: Optional[float] = Field(None, ge=0)
    cholesterol: Optional[float] = Field(None, ge=0)
    saturated_fatty_acids: Optional[float] = Field(None, ge=0)
    trans_fat: Optional[float] = Field(None, ge=0)

    @field_validator('research_year')
    @classmethod
    def validate_year(cls, v):
        if v is not None and not re.match(r'^\d{4}$', v):
            raise ValueError('연도는 YYYY 형식이어야 합니다')
        if v is not None:
            year = int(v)
            if year < 1900 or year > 2100:
                raise ValueError('연도는 1900년과 2100년 사이여야 합니다')
        return v


class FoodResponse(FoodBase):
    """식품 응답 스키마"""
    id: int = Field(..., description="식품 ID")
    
    model_config = ConfigDict(from_attributes=True)


class FoodSearchParams(BaseModel):
    """식품 검색 파라미터 스키마"""
    food_name: Optional[str] = Field(None, description="식품이름 (부분 일치 검색)")
    research_year: Optional[str] = Field(None, pattern=r'^\d{4}$', description="연도(YYYY)")
    maker_name: Optional[str] = Field(None, description="지역/제조사")
    food_code: Optional[str] = Field(None, description="식품코드")

    @field_validator('research_year')
    @classmethod
    def validate_year(cls, v):
        if v is not None and not re.match(r'^\d{4}$', v):
            raise ValueError('연도는 YYYY 형식이어야 합니다')
        return v


class PaginationParams(BaseModel):
    """페이지네이션 파라미터 스키마"""
    page: int = Field(default=1, ge=1, description="페이지 번호")
    limit: int = Field(default=20, ge=1, le=100, description="페이지당 항목 수")


class PaginationInfo(BaseModel):
    """페이지네이션 정보 스키마"""
    page: int
    limit: int
    total: int
    totalPages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """페이지네이션된 응답 스키마"""
    status: str = "success"
    data: List[T]
    pagination: PaginationInfo


class ApiResponse(BaseModel, Generic[T]):
    """일반 API 응답 스키마"""
    status: str = "success"
    data: T


class ApiListResponse(BaseModel, Generic[T]):
    """리스트 API 응답 스키마"""
    status: str = "success"
    data: List[T]
    count: int


class ErrorDetail(BaseModel):
    """에러 상세 정보 스키마"""
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    status: str = "error"
    error: ErrorDetail