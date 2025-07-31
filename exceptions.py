from fastapi import HTTPException, status


class FoodAPIException(HTTPException):
    """식품 API 기본 예외 클래스"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class FoodNotFoundError(FoodAPIException):
    """식품을 찾을 수 없는 경우 예외"""
    def __init__(self, food_id: int = None, food_cd: str = None):
        detail = "요청한 식품 정보를 찾을 수 없습니다."
        if food_id:
            detail = f"ID {food_id}인 식품을 찾을 수 없습니다."
        elif food_cd:
            detail = f"식품코드 {food_cd}인 식품을 찾을 수 없습니다."
        
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND"
        )


class FoodAlreadyExistsError(FoodAPIException):
    """식품이 이미 존재하는 경우 예외"""
    def __init__(self, food_cd: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"식품코드 {food_cd}는 이미 존재합니다.",
            error_code="RESOURCE_ALREADY_EXISTS"
        )


class ValidationError(FoodAPIException):
    """유효성 검증 실패 예외"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class DatabaseError(FoodAPIException):
    """데이터베이스 오류 예외"""
    def __init__(self, detail: str = "데이터베이스 오류가 발생했습니다."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )