import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="기능/자료 요청", page_icon="💡", layout="wide")

st.title("💡 기능 및 자료 요청")

# 1. 구글 시트 연결 설정 (JSON 파일 직접 로드)
# ※ google_key.json 파일이 my_portal 폴더 안에 있어야 합니다.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    # 서비스 계정 키 파일로 인증
    creds = Credentials.from_service_account_file("google_key.json", scopes=scope)
    client = gspread.authorize(creds)
    
    # 구글 시트 열기 (본인의 시트 이름을 정확히 적으세요)
    # URL로 여는 것이 가장 정확합니다.
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1r9tZzD4UWyv1OfUJZBdUG8-29L3yuc0E-UNKnXm3sNc/edit"
    spreadsheet = client.open_by_url(SHEET_URL)
    sheet = spreadsheet.get_worksheet(0) # 첫 번째 탭

    with st.form("request_form"):
        st.subheader("📝 요청 사항 입력")
        request_type = st.selectbox("요청 분류", ["계산기 추가", "매뉴얼 요청", "양식/서식 요청", "기타 건의"])
        title = st.text_input("제목")
        content = st.text_area("상세 내용")
        submitted = st.form_submit_button("요청 제출하기")
        
        if submitted:
            if title.strip() and content.strip():
                # 새 데이터 행 생성
                new_row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    request_type,
                    title,
                    content
                ]
                
                # 구글 시트에 한 줄 추가
                sheet.append_row(new_row)
                
                st.success("✅ 구글 시트에 성공적으로 저장되었습니다!")
                st.balloons()
            else:
                st.error("❌ 제목과 내용을 모두 입력해 주세요.")

    # 최근 데이터 표시
    st.markdown("---")
    st.subheader("📋 최근 접수 현황")
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df.iloc[::-1].head(10), use_container_width=True)
    else:
        st.info("아직 접수된 내역이 없습니다.")

except Exception as e:
    st.error("⚠️ 연결 오류가 발생했습니다.")
    st.info(f"에러 내용: {e}")
    st.write("1. google_key.json 파일이 서버에 있는지 확인해 주세요.")
    st.write("2. 구글 시트에서 서비스 계정 이메일을 '편집자'로 초대했는지 확인해 주세요.")