import streamlit as st
import streamlit.components.v1 as components
import os

# --- [0단계] 가상 파일 응답 로직 ---
google_file_name = "googleac826ba707a1db10" 
if st.query_params.get("page") == "robots":
    st.text("User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /")
    st.stop()
elif st.query_params.get("page") == google_file_name:
    st.write(f"google-site-verification: {google_file_name}.html")
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="VoltMaster - 전력 운용 포털", 
    page_icon="⚡", 
    layout="wide"
)

# --- [1단계] 구글 인증 및 애드센스 ---
verification_code = "uXxXH_PzU8GwoKbIjxKaFuGOCuYV7EWnk3wr9b9OtrM"
adsense_id = "ca-pub-9577213309229562"
st.markdown(f"""
    <div style="display: none;">
        <meta name="google-adsense-account" content="{adsense_id}">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_id}" crossorigin="anonymous"></script>
        <meta name="google-site-verification" content="{verification_code}" />
    </div>
""", unsafe_allow_html=True)

# --- [2단계] 정적 파일 생성 ---
if not os.path.exists("static"): os.makedirs("static")
with open("static/robots.txt", "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /")

# --- [3단계] 디자인: CSS (복구 버전) ---
st.markdown("""
    <style>
        /* 기본 네비게이션 스타일링 */
        div[data-testid="stSidebarNavViewButton"] { display: none !important; }
        div[data-testid="stSidebarNavSeparator"] { display: none !important; }
        
        .main-title { font-size: 3.2rem; color: #FFD700; text-align: center; text-shadow: 2px 2px 4px #000000; }
        .sub-title { font-size: 1.2rem; color: #AAAAAA; text-align: center; padding-bottom: 2rem; }
        
        /* 푸터 구분선 및 간격 스타일 */
        hr { margin-top: 2.5rem !important; margin-bottom: 1rem !important; border: 0; border-top: 1px solid #444; }
        div[data-testid="column"] { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

def render_main_home():
    st.markdown('<h1 class="main-title">⚡ VoltMaster</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Data Center Power Infrastructure Engineering Portal</p>', unsafe_allow_html=True)
    st.caption("공고")
    components.html("""<div style='background-color: #262730; color: #555; text-align: center; padding: 10px;'>광고 영역</div>""", height=50)
    st.markdown("### 🚀 Core Engineering Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background-color: #1E1E1E; padding: 25px; border-radius: 15px; border-left: 6px solid #FFD700; height: 180px; margin-bottom: 10px;"><h2 style="color: white;">🧮 1. 실무 전력 계산기</h2><p style="color: #BBBBBB;">데이터센터 현장 실무 12개 모듈</p></div>', unsafe_allow_html=True)
        if st.button("계산기 엔진 기동 🏎️", use_container_width=True, type="primary", key="btn_calc"): st.switch_page("pages/1_calculator.py")
    with col2:
        st.markdown('<div style="background-color: #1E1E1E; padding: 25px; border-radius: 15px; border-left: 6px solid #00BFFF; height: 180px; margin-bottom: 10px;"><h2 style="color: white;">🤖 2. AI 자격증 튜터</h2><p style="color: #BBBBBB;">건축전기기술사 및 전기분야 자격증 학습</p></div>', unsafe_allow_html=True)
        if st.button("AI 튜터와 학습 시작 📚", use_container_width=True, type="primary", key="btn_tutor"): st.switch_page("pages/2_ai_tutor.py")
    st.divider()

# --- [5단계] 내비게이션 설정 (소통 및 고객지원 통합 버전) ---
pages_dict = {
    "": [
        st.Page(render_main_home, title="⚡ VoltMaster 홈", default=True),
        st.Page("pages/1_calculator.py", title="🧮 실무 전력 계산기"),
    ],
    "✨ AI 자격증 튜터": [
        st.Page("pages/2_ai_tutor.py", title="✨ AI 튜터 메인/통계"),
        st.Page("tutor/1_professional.py", title="🥇 건축전기설비기술사"),
        st.Page("tutor/2_engineer.py", title="🥈 전기기사"),
        st.Page("tutor/3_industrial.py", title="🥉 전기산업기사"),
        st.Page("tutor/4_craftsman.py", title="🎖️ 전기기능사"),
    ],
    "📁 자료 및 정보": [
        st.Page("pages/3_manuals.py", title="📚 설비 아카이브"),
        st.Page("pages/4_templates.py", title="📝 현장 점검 양식"),
        st.Page("pages/5_kec_search.py", title="🔍 KEC 스마트 검색기"),
        st.Page("pages/6_blog_events.py", title="☕ 전기인의 핫플 & 트렌드"),
    ],
    "📢 소통 및 고객지원": [
        st.Page("pages/7_notice.py", title="🔔 공지사항"),
        st.Page("pages/8_free_board.py", title="💬 자유게시판"),
        st.Page("pages/9_request_board.py", title="💡 기능/자료 요청"),
        st.Page("pages/10_contact.py", title="📧 문의하기"),
        st.Page("pages/0_privacy_policy.py", title="📃 개인정보 처리방침 및 약관"),
    ]
}

if st.query_params.get("manage") == "true" or st.session_state.get("is_admin", False):
    st.session_state.is_admin = True
    pages_dict["🔐 시스템 관리"] = [st.Page("pages/admin_notice.py", title="공지사항 관리", icon="⚙️")]

# --- [6단계] 실행 ---
pg = st.navigation(pages_dict)
pg.run()

# --- 푸터 영역 ---
st.divider()

_, footer_col = st.columns([6, 4])
with footer_col:
    st.markdown('''
        <div style="text-align: right; line-height: 1.4; font-size: 0.8rem; color: #777; margin-top: 5px;">
            <p style="margin-bottom: 3px;">© 2026 <b>VoltMaster. All rights reserved.</b></p>
            <p style="margin-bottom: 3px;">
                <a href="/privacy_policy" target="_self" style="text-decoration: none; color: #007bff; font-weight: bold;">
                    개인정보 처리방침 및 약관
                </a>
            </p>
            <p style="margin-bottom: 3px;">
                Contact: <a href="mailto:jiyong-na@naver.com" style="text-decoration: none; color: inherit;">jiyong-na@naver.com</a>
            </p>
            <p style="margin-bottom: 0;">VoltMaster 운영팀</p>
        </div>
    ''', unsafe_allow_html=True)