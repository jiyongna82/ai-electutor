import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. 페이지 설정
st.set_page_config(page_title="문의하기 | VoltMaster", page_icon="📧", layout="wide")

# 2. 구글 시트 연동 함수
def append_to_gsheet(data_list):
    try:
        # 인증 범위 설정
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # google_key.json 파일 로드 (파일이 같은 경로에 있어야 함)
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_key.json", scope)
        client = gspread.authorize(creds)
        
        # 시트 이름으로 열기
        sheet = client.open("VoltMaster_Contact").sheet1
        sheet.append_row(data_list)
        return True
    except Exception as e:
        st.error(f"데이터 전송 중 오류 발생: {e}")
        return False

# 3. 타이틀 및 브랜딩
st.title("📧 VoltMaster 문의하기")
st.markdown("""
**VoltMaster**는 전기 기술인들의 더 나은 실무 환경을 위해 언제나 열려 있습니다.  
전송 버튼을 누르는 순간, 운영팀의 단말기로 **무손실 데이터**가 전달됩니다. ⚡
""")

st.success("💡 **비즈니스 제휴 및 기술 자문 문의**는 아래 폼을 이용하시거나 공식 이메일로 연락 주시면 광속으로 회신드립니다.")
st.divider()

# 4. 문의 채널 안내 카드
col1, col2, col3 = st.columns(3)
contact_info = {
    "🤝 제휴 및 협업": "기술 세미나, 콘텐츠 제휴, 광고 제휴",
    "🛠️ 기술 자문/교육": "전력 계통 분석, KEC 설계, 데이터센터 교육",
    "💡 서비스 개선": "VoltMaster 기능 제안 및 오류 제보"
}

for col, (title, desc) in zip([col1, col2, col3], contact_info.items()):
    with col:
        with st.container(border=True):
            st.subheader(title)
            st.write(desc)
            st.caption("✉️ jiyong-na@naver.com")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 1:1 메시지 전송 폼
st.subheader("📨 1:1 메시지 보내기")

with st.form("contact_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("성함/기업명", placeholder="문의하시는 분의 성함")
    with c2:
        contact = st.text_input("연락처/이메일", placeholder="답변받으실 이메일 주소나 연락처")
    
    category = st.selectbox("문의 유형", ["비즈니스 협업", "기술 자문 의뢰", "콘텐츠 오타 제보", "기타 제안"])
    subject = st.text_input("문의 제목", placeholder="제목을 입력하세요.")
    message = st.text_area("문의 상세 내용", placeholder="내용을 상세히 적어주시면 검토 후 신속히 연락드리겠습니다.", height=200)
    
    submitted = st.form_submit_button("메시지 전송하기")
    
    if submitted:
        if name and contact and message:
            # 저장할 데이터 리스트 생성
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_to_save = [now, name, contact, category, subject, message]
            
            # 구글 시트에 데이터 추가
            with st.spinner("VoltMaster 전력망을 통해 데이터를 전송 중..."):
                if append_to_gsheet(data_to_save):
                    st.balloons()
                    st.success(f"✅ 전송 완료! {name} 님의 문의가 성공적으로 접수되었습니다. 곧 회신드리겠습니다.")
        else:
            st.error("⚠️ 필수 항목(성함, 연락처, 내용)을 모두 입력해 주세요.")

st.divider()

# 6. 하단 푸터
st.markdown(
    """<div style="text-align: center; opacity: 0.5; font-size: 11px; color: gray;">
    © 2026 VoltMaster. All rights reserved.
    </div>""", 
    unsafe_allow_html=True
)