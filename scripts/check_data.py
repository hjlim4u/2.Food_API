import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
sys.path.append(str(Path(__file__).parent.parent))

from database import async_session_factory
from sqlalchemy import text

async def check_data():
    """데이터베이스의 데이터를 확인합니다."""
    async with async_session_factory() as session:
        # 총 개수 확인
        result = await session.execute(text('SELECT COUNT(*) FROM foods'))
        total_count = result.scalar()
        print(f'총 식품 데이터: {total_count:,}개')
        
        # 샘플 데이터 확인
        result = await session.execute(text('SELECT food_cd, food_name, research_year, calorie FROM foods LIMIT 5'))
        rows = result.fetchall()
        
        print('\n샘플 데이터:')
        print('식품코드 | 식품명 | 연도 | 칼로리')
        print('-' * 50)
        for row in rows:
            print(f'{row[0]} | {row[1][:20]:<20} | {row[2]} | {row[3]}')

if __name__ == "__main__":
    asyncio.run(check_data())