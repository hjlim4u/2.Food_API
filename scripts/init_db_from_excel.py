import asyncio
import argparse
import pandas as pd
import sys
import os
from pathlib import Path
import logging

# 프로젝트 루트를 Python path에 추가
sys.path.append(str(Path(__file__).parent.parent))

from database import async_session_factory, create_tables
from repositories.food_repository import FoodRepository
from schemas.food import FoodCreate
from models.food import Food
from sqlalchemy import text

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def init_from_excel(excel_path: str, clear_existing: bool = False):
    """엑셀 파일로부터 데이터베이스를 초기화합니다."""
    
    logger.info("데이터베이스 테이블 생성 중...")
    await create_tables()
    
    # 엑셀 파일 읽기
    try:
        logger.info(f"엑셀 파일 읽기 중: {excel_path}")
        df = pd.read_excel(excel_path)
        logger.info(f"엑셀 파일에서 {len(df)}개 행을 읽었습니다.")
    except Exception as e:
        logger.error(f"엑셀 파일 읽기 실패: {e}")
        return
    
    async with async_session_factory() as session:
        try:
            # 기존 데이터 삭제
            if clear_existing:
                logger.info("기존 데이터 삭제 중...")
                await session.execute(text("DELETE FROM foods"))
                await session.commit()
                logger.info("기존 데이터를 삭제했습니다.")
            
            repository = FoodRepository(session)
            success_count = 0
            error_count = 0
            
            # 배치 처리
            batch_size = 100
            total_batches = (len(df) + batch_size - 1) // batch_size
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch_num = i // batch_size + 1
                logger.info(f"배치 {batch_num}/{total_batches} 처리 중... ({i+1}-{min(i+batch_size, len(df))})")
                
                for index, row in batch.iterrows():
                    try:
                        # 데이터 검증 및 변환
                        def safe_str(value):
                            """안전하게 문자열로 변환"""
                            if pd.isna(value) or value == '-':
                                return ""
                            return str(value).strip()
                        
                        def safe_float(value):
                            """안전하게 float로 변환"""
                            if pd.isna(value) or value == '-' or value == '':
                                return 0.0
                            try:
                                return float(value)
                            except (ValueError, TypeError):
                                return 0.0
                        
                        # 필수 필드 검증
                        food_cd = safe_str(row['식품코드'])
                        food_name = safe_str(row['식품명'])
                        research_year = safe_str(row['연도'])
                        
                        if not food_cd or not food_name:
                            logger.warning(f"Row {index + 1}: 필수 필드 누락 (식품코드: {food_cd}, 식품명: {food_name})")
                            error_count += 1
                            continue
                        
                        # 연도 형식 검증
                        if not research_year or len(research_year) != 4 or not research_year.isdigit():
                            research_year = "2023"  # 기본값 설정
                        
                        food_data = FoodCreate(
                            food_cd=food_cd,
                            group_name=safe_str(row['DB군']),
                            food_name=food_name,
                            research_year=research_year,
                            maker_name=safe_str(row['지역 / 제조사']),
                            ref_name=safe_str(row['성분표출처']),
                            serving_size=safe_str(row['1회제공량']),
                            calorie=safe_float(row['에너지(㎉)']),
                            carbohydrate=safe_float(row['탄수화물(g)']),
                            protein=safe_float(row['단백질(g)']),
                            province=safe_float(row['지방(g)']),
                            sugars=safe_float(row['총당류(g)']),
                            salt=safe_float(row['나트륨(㎎)']),
                            cholesterol=safe_float(row['콜레스테롤(㎎)']),
                            saturated_fatty_acids=safe_float(row['총 포화 지방산(g)']),
                            trans_fat=safe_float(row['트랜스 지방산(g)'])
                        )
                        
                        await repository.create(food_data)
                        success_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        logger.warning(f"Row {index + 1} 처리 실패: {e}")
                
                # 배치마다 커밋
                await session.commit()
                logger.info(f"배치 {batch_num} 완료 - 성공: {success_count}, 실패: {error_count}")
            
            logger.info(f"\n초기화 완료!")
            logger.info(f"성공: {success_count}개")
            logger.info(f"실패: {error_count}개")
            logger.info(f"총 처리율: {success_count/(success_count+error_count)*100:.1f}%")
            
        except Exception as e:
            await session.rollback()
            logger.error(f"초기화 실패: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description='엑셀 파일로부터 데이터베이스 초기화')
    parser.add_argument('excel_path', nargs='?', help='엑셀 파일 경로 (미지정 시 자동 검색)')
    parser.add_argument('--clear', action='store_true', help='기존 데이터 삭제')
    
    args = parser.parse_args()
    
    # 엑셀 파일 경로 결정
    if args.excel_path:
        excel_path = args.excel_path
    else:
        # 프로젝트 루트의 food_nutrition_db.xlsx 파일 사용
        excel_path = "../food_nutrition_db.xlsx"
        if not os.path.exists(excel_path):
            print(f"엑셀 파일을 찾을 수 없습니다: {excel_path}")
            print("프로젝트 루트에 food_nutrition_db.xlsx 파일이 있는지 확인해주세요.")
            print("사용법: python scripts/init_db_from_excel.py [excel_file_path] [--clear]")
            return
        print(f"엑셀 파일을 사용합니다: {excel_path}")
    
    if not os.path.exists(excel_path):
        print(f"파일을 찾을 수 없습니다: {excel_path}")
        return
    
    if args.clear:
        response = input("기존 데이터를 모두 삭제하고 초기화하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("초기화를 취소했습니다.")
            return
    
    asyncio.run(init_from_excel(excel_path, args.clear))

if __name__ == "__main__":
    main()