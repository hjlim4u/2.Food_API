from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import ValidationError
import logging

import os

from database import create_tables, async_session_factory
from routers.food import router as food_router
from exceptions import FoodAPIException
from middleware import (
    food_api_exception_handler,
    validation_exception_handler,
    http_exception_handler_custom,
    general_exception_handler
)
from sqlalchemy import func, select
from models.food import Food
# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def auto_initialize_data():
    """데이터가 없으면 자동으로 엑셀에서 초기화"""
    async with async_session_factory() as session:
        try:
            # 데이터 개수 확인
            result = await session.execute(select(func.count(Food.id)))
            count = result.scalar()
            
            if count == 0:
                logger.info("데이터베이스가 비어있습니다. 엑셀 파일에서 초기화를 시작합니다...")
                
                # 프로젝트 루트의 food_nutrition_db.xlsx 파일 사용
                excel_path = "food_nutrition_db.xlsx"
                if os.path.exists(excel_path):
                    logger.info(f"엑셀 파일 사용: {excel_path}")
                    
                    # 동적으로 초기화 스크립트 임포트 및 실행
                    from scripts.init_db_from_excel import init_from_excel
                    await init_from_excel(excel_path, clear_existing=False)
                    logger.info("엑셀 데이터 초기화가 완료되었습니다.")
                else:
                    logger.warning(f"초기화용 엑셀 파일을 찾을 수 없습니다: {excel_path}")
                    logger.warning("프로젝트 루트에 food_nutrition_db.xlsx 파일이 있는지 확인해주세요.")
            else:
                logger.info(f"데이터베이스에 {count}개의 식품 데이터가 있습니다.")
                
        except Exception as e:
            logger.error(f"자동 초기화 중 오류 발생: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트 처리"""
    # 시작 시
    logger.info("애플리케이션을 시작합니다...")
    await create_tables()
    logger.info("데이터베이스 테이블이 생성되었습니다.")
    
    # 데이터가 없으면 엑셀에서 자동 초기화
    await auto_initialize_data()
    
    yield
    
    # 종료 시
    logger.info("애플리케이션을 종료합니다...")


app = FastAPI(
    title="Food API",
    description="식품 영양 정보 RESTful API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영환경에서는 실제 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 예외 핸들러 등록
app.add_exception_handler(FoodAPIException, food_api_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler_custom)
app.add_exception_handler(Exception, general_exception_handler)

# 라우터 등록
app.include_router(food_router)


@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "Food Nutrition API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy"}
