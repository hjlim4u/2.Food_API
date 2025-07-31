from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class Food(Base):
    """식품 정보 모델"""
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    food_cd = Column(String(50), unique=True, nullable=False, index=True)
    group_name = Column(String(100), nullable=False)
    food_name = Column(String(200), nullable=False, index=True)
    research_year = Column(String(4), nullable=False, index=True)
    maker_name = Column(String(100), nullable=False, index=True)
    ref_name = Column(String(100), nullable=False)
    serving_size = Column(String(50), nullable=False)
    calorie = Column(Float, nullable=False)
    carbohydrate = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    province = Column(Float, nullable=False)  # 지방 (fat)
    sugars = Column(Float, nullable=False)
    salt = Column(Float, nullable=False)  # 나트륨 (sodium)
    cholesterol = Column(Float, nullable=False)
    saturated_fatty_acids = Column(Float, nullable=False)
    trans_fat = Column(Float, nullable=False)
    
    # 생성/수정 시간 (선택사항)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Food(id={self.id}, food_cd='{self.food_cd}', food_name='{self.food_name}')>"