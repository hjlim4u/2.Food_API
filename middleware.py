from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from pydantic import ValidationError
from exceptions import FoodAPIException
from schemas.food import ErrorResponse, ErrorDetail
import logging

logger = logging.getLogger(__name__)


async def food_api_exception_handler(request: Request, exc: FoodAPIException):
    """커스텀 Food API 예외 핸들러"""
    logger.error(f"Food API Exception: {exc.detail}")
    
    error_detail = ErrorDetail(
        code=exc.error_code or "UNKNOWN_ERROR",
        message=exc.detail,
        details=getattr(exc, 'details', None)
    )
    
    error_response = ErrorResponse(error=error_detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Pydantic 유효성 검증 예외 핸들러"""
    logger.error(f"Validation Error: {exc.errors()}")
    
    error_detail = ErrorDetail(
        code="VALIDATION_ERROR",
        message="입력 데이터 유효성 검증에 실패했습니다.",
        details={"errors": exc.errors()}
    )
    
    error_response = ErrorResponse(error=error_detail)
    
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


async def http_exception_handler_custom(request: Request, exc: HTTPException):
    """HTTP 예외 핸들러"""
    logger.error(f"HTTP Exception: {exc.detail}")
    
    # 이미 FoodAPIException 형태라면 그대로 처리
    if hasattr(exc, 'error_code'):
        return await food_api_exception_handler(request, exc)
    
    error_detail = ErrorDetail(
        code="HTTP_ERROR",
        message=exc.detail
    )
    
    error_response = ErrorResponse(error=error_detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    error_detail = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        message="서버 내부 오류가 발생했습니다."
    )
    
    error_response = ErrorResponse(error=error_detail)
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )