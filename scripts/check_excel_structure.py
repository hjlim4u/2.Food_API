import pandas as pd
import sys
import os

def check_excel_structure(excel_path: str):
    """엑셀 파일의 구조를 확인합니다."""
    try:
        print(f"엑셀 파일 분석 중: {excel_path}")
        
        # 엑셀 파일 읽기
        df = pd.read_excel(excel_path)
        
        print(f"\n총 행 수: {len(df)}")
        print(f"총 열 수: {len(df.columns)}")
        
        print("\n컬럼명:")
        for i, col in enumerate(df.columns):
            print(f"{i+1:2d}. {col}")
        
        print("\n첫 5행 데이터:")
        print(df.head())
        
        print("\n데이터 타입:")
        print(df.dtypes)
        
        print("\n결측값 확인:")
        print(df.isnull().sum())
        
    except Exception as e:
        print(f"엑셀 파일 분석 실패: {e}")

if __name__ == "__main__":
    # 프로젝트 루트의 food_nutrition_db.xlsx 파일 사용
    excel_path = "../food_nutrition_db.xlsx"
    if os.path.exists(excel_path):
        print(f"엑셀 파일 사용: {excel_path}")
        check_excel_structure(excel_path)
    else:
        print(f"엑셀 파일을 찾을 수 없습니다: {excel_path}")
        print("프로젝트 루트에 food_nutrition_db.xlsx 파일이 있는지 확인해주세요.")