# Food API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

식품 영양 정보를 관리하는 RESTful API입니다. FastAPI 기반으로 구축되었으며, Excel 파일에서 자동으로 데이터를 초기화하고 완전한 CRUD 기능을 제공합니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [API 엔드포인트](#api-엔드포인트)
- [설치 및 실행](#설치-및-실행)
- [사용 예시](#사용-예시)
- [RESTful API 모범 사례](#restful-api-모범-사례)
- [개발 가이드](#개발-가이드)

## 🚀 주요 기능

- **완전한 CRUD 작업**: 식품 정보의 생성, 조회, 수정, 삭제
- **고급 검색**: 식품명, 연도, 제조사, 식품코드로 검색
- **페이지네이션**: 대용량 데이터 효율적 처리
- **자동 데이터 초기화**: Excel 파일에서 자동 데이터베이스 초기화
- **데이터 검증**: Pydantic을 활용한 강력한 입력 검증
- **API 문서화**: 자동 생성되는 OpenAPI/Swagger 문서
- **컨테이너화**: Docker 및 Docker Compose 지원
- **헬스체크**: 애플리케이션 상태 모니터링

## 🛠 기술 스택

### 백엔드
- **FastAPI**: 현대적이고 빠른 Python 웹 프레임워크
- **SQLAlchemy 2.0**: 비동기 ORM
- **Pydantic 2.0**: 데이터 검증 및 설정 관리
- **uvicorn**: ASGI 서버

### 데이터베이스
- **SQLite**: 개발 환경용 (기본)

### 기타
- **Docker**: 컨테이너화
- **Pandas**: Excel 데이터 처리
- **pytest**: 테스트 (예정)

## 📁 프로젝트 구조

```
2.foodAPI/
├── main.py                 # FastAPI 애플리케이션 진입점
├── database.py            # 데이터베이스 설정
├── dependencies.py        # 의존성 주입
├── exceptions.py          # 커스텀 예외
├── middleware.py          # 미들웨어 및 예외 핸들러
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 이미지 설정
├── docker-compose.yml    # Docker Compose 설정
├── food_nutrition_db.xlsx # 초기 데이터 Excel 파일
├── test_main.http        # API 테스트 파일
├── models/               # SQLAlchemy 모델
│   └── food.py
├── schemas/              # Pydantic 스키마
│   └── food.py
├── repositories/         # 데이터 접근 레이어
│   └── food_repository.py
├── routers/              # API 라우터
│   └── food.py
└── scripts/              # 유틸리티 스크립트
    ├── init_db_from_excel.py
    ├── check_data.py
    └── check_excel_structure.py
```

## 🔗 API 엔드포인트

### 기본 엔드포인트
- `GET /` - API 정보
- `GET /health` - 헬스체크
- `GET /docs` - Swagger UI 문서
- `GET /redoc` - ReDoc 문서

### 식품 관리 API (`/v1/foods`)

| 메소드 | 엔드포인트 | 설명 | 응답 코드 |
|--------|-----------|------|----------|
| `GET` | `/v1/foods` | 식품 목록 조회 (페이지네이션) | 200 |
| `GET` | `/v1/foods/search` | 식품 검색 | 200 |
| `GET` | `/v1/foods/{id}` | 특정 식품 조회 | 200, 404 |
| `POST` | `/v1/foods` | 새 식품 등록 | 201, 400, 409 |
| `PUT` | `/v1/foods/{id}` | 식품 전체 수정 | 200, 400, 404 |
| `PATCH` | `/v1/foods/{id}` | 식품 부분 수정 | 200, 400, 404 |
| `DELETE` | `/v1/foods/{id}` | 식품 삭제 | 204, 404 |

### 쿼리 파라미터

#### 페이지네이션 (`GET /v1/foods`)
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20, 최대: 100)

#### 검색 (`GET /v1/foods/search`)
- `food_name`: 식품명 (부분 일치)
- `research_year`: 연도 (YYYY 형식)
- `maker_name`: 제조사/지역
- `food_code`: 식품코드

## 🚀 설치 및 실행

### 1. Docker를 사용한 실행 (권장)

```bash
# 저장소 클론
git clone <repository-url>
cd 2.foodAPI

# Docker Compose로 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f food-api
```

### 2. 로컬 환경에서 실행

```bash
# Python 3.11+ 필요
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 데이터베이스 초기화

애플리케이션 실행 시 `food_nutrition_db.xlsx` 파일이 프로젝트 루트에 있으면 자동으로 데이터베이스가 초기화됩니다.

#### 자동 초기화
- 애플리케이션 시작 시 Excel 파일을 자동으로 감지하여 데이터베이스 초기화
- 기존 데이터가 있으면 추가로 데이터를 삽입 (중복 방지)

#### 수동 초기화
Excel 파일을 수동으로 처리하거나 기존 데이터를 완전히 초기화하려면:

```bash
# 기본 실행 (기존 데이터 유지, 새 데이터 추가)
python scripts/init_db_from_excel.py

# 기존 데이터 완전 삭제 후 초기화
python scripts/init_db_from_excel.py --clear

# 특정 Excel 파일 지정
python scripts/init_db_from_excel.py path/to/your/excel_file.xlsx

# 특정 Excel 파일로 완전 초기화
python scripts/init_db_from_excel.py path/to/your/excel_file.xlsx --clear
```

#### 초기화 스크립트 옵션
- `--clear`: 기존 데이터를 모두 삭제하고 새로 초기화
- 파일 경로 미지정 시: 프로젝트 루트의 `food_nutrition_db.xlsx` 사용
- 배치 처리로 대용량 데이터 효율적 처리
- 상세한 로그 출력으로 진행 상황 확인

### 4. 접속 확인

- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/health

## 📝 사용 예시

### 1. 식품 목록 조회
```bash
curl "http://localhost:8000/v1/foods?page=1&limit=20"
```

### 2. 식품 검색
```bash
curl "http://localhost:8000/v1/foods/search?food_name=김치&research_year=2023"
```

### 3. 새 식품 등록
```bash
curl -X POST "http://localhost:8000/v1/foods" \
     -H "Content-Type: application/json" \
     -d '{
       "food_cd": "F001234",
       "group_name": "김치류",
       "food_name": "배추김치",
       "research_year": "2023",
       "maker_name": "서울",
       "ref_name": "국민영양조사",
       "serving_size": "100g",
       "calorie": 25.5,
       "carbohydrate": 4.2,
       "protein": 1.8,
       "province": 0.5,
       "sugars": 2.1,
       "salt": 850,
       "cholesterol": 0,
       "saturated_fatty_acids": 0.1,
       "trans_fat": 0
     }'
```

### 4. 식품 부분 수정
```bash
curl -X PATCH "http://localhost:8000/v1/foods/1" \
     -H "Content-Type: application/json" \
     -d '{
       "calorie": 26.5,
       "protein": 2.0
     }'
```

## 🎯 RESTful API 모범 사례

이 프로젝트는 다음과 같은 RESTful API 모범 사례를 구현합니다:

### 1. HTTP 메소드 적절한 사용
- **GET**: 데이터 조회 (멱등성)
- **POST**: 새 리소스 생성
- **PUT**: 전체 리소스 수정 (멱등성)
- **PATCH**: 부분 리소스 수정
- **DELETE**: 리소스 삭제 (멱등성)

### 2. 적절한 HTTP 상태 코드
- **200 OK**: 성공적인 조회/수정
- **201 Created**: 리소스 생성 성공
- **204 No Content**: 성공적인 삭제
- **400 Bad Request**: 잘못된 요청
- **404 Not Found**: 리소스 없음
- **409 Conflict**: 리소스 충돌
- **422 Unprocessable Entity**: 검증 오류

### 3. RESTful URL 설계
```
GET    /v1/foods           # 식품 목록
GET    /v1/foods/{id}      # 특정 식품 조회
POST   /v1/foods           # 새 식품 생성
PUT    /v1/foods/{id}      # 식품 전체 수정
PATCH  /v1/foods/{id}      # 식품 부분 수정
DELETE /v1/foods/{id}      # 식품 삭제
GET    /v1/foods/search    # 식품 검색
```

### 4. 일관된 응답 구조
```json
{
  "status": "success",
  "data": {...},
  "pagination": {...}  // 페이지네이션이 있는 경우
}
```

### 5. 데이터 검증
- **Pydantic 스키마**: 입력 데이터 자동 검증
- **타입 힌트**: 명확한 데이터 타입 정의
- **커스텀 검증**: 비즈니스 로직 검증 (연도 범위 등)

### 6. 에러 처리
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력 데이터가 올바르지 않습니다",
    "details": {...}
  }
}
```

### 7. API 버전 관리
- URL 경로에 버전 포함: `/v1/foods`
- 하위 호환성 유지

### 8. 페이지네이션
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 9. 검색 및 필터링
- 쿼리 파라미터 사용
- 부분 일치 검색 지원
- 다중 검색 조건 조합

### 10. 문서화
- **자동 생성**: OpenAPI/Swagger 문서
- **상세 설명**: 각 엔드포인트별 설명
- **예시 포함**: 요청/응답 예시

## 🔧 개발 가이드

### 환경 변수
```bash
DATABASE_URL=sqlite+aiosqlite:///./data/food_api.db  # 데이터베이스 URL
HOST=0.0.0.0                                         # 서버 호스트
PORT=8000                                            # 서버 포트
WORKERS=1                                            # 워커 프로세스 수
```

### 데이터베이스 초기화

#### 자동 초기화
Excel 파일(`food_nutrition_db.xlsx`)이 프로젝트 루트에 있으면 애플리케이션 시작 시 자동으로 데이터가 초기화됩니다.

#### 수동 초기화 스크립트
```bash
# 기본 초기화 (기존 데이터 유지)
python scripts/init_db_from_excel.py

# 완전 초기화 (기존 데이터 삭제)
python scripts/init_db_from_excel.py --clear

# 특정 파일로 초기화
python scripts/init_db_from_excel.py your_data.xlsx
```

#### 초기화 스크립트 특징
- **배치 처리**: 대용량 데이터 효율적 처리 (100개씩 배치)
- **데이터 검증**: 필수 필드 검증 및 타입 변환
- **에러 처리**: 개별 행 처리 실패 시에도 전체 프로세스 계속
- **상세 로깅**: 진행 상황 및 성공/실패 통계 출력
- **안전한 변환**: Excel의 빈 값, '-' 등을 안전하게 처리

### 코드 구조 설명

#### 레이어드 아키텍처
1. **Routers**: HTTP 요청 처리 및 응답
2. **Repositories**: 데이터 접근 로직
3. **Models**: 데이터베이스 모델 (SQLAlchemy)
4. **Schemas**: 데이터 검증 및 직렬화 (Pydantic)

#### 의존성 주입
```python
# dependencies.py
async def get_food_repository() -> FoodRepository:
    async with async_session_factory() as session:
        yield FoodRepository(session)
```

#### 예외 처리
```python
# 커스텀 예외 정의
class FoodAPIException(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details
```

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [REST API 설계 가이드](https://restfulapi.net/)
- [HTTP 상태 코드](https://developer.mozilla.org/ko/docs/Web/HTTP/Status)


---