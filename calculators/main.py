import streamlit as st
import importlib.util
import os

st.set_page_config(page_title="VoltMaster 통합 계산기", layout="wide")

# URL에서 계산기 ID를 가져옵니다 (예: ?id=1-1)
query_params = st.query_params
calc_id = query_params.get("id", "1-1")

def load_and_run(file_id):
    file_name = f"calc_{file_id}.py"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    
    if os.path.exists(file_path):
        # 파일을 모듈로 동적 로드
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 만약 파일 내부에 run_calc() 함수가 있다면 실행
        if hasattr(module, 'run_calc'):
            module.run_calc()
        else:
            # 함수화가 안 되어 있는 경우를 대비한 처리
            st.warning(f"{file_name} 파일에 run_calc() 함수가 없습니다.")
    else:
        st.error(f"계산기 파일({file_name})을 찾을 수 없습니다.")

load_and_run(calc_id)