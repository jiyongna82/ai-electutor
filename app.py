import streamlit as st
import streamlit.components.v1 as components
import os

# [중요] 페이지 설정은 항상 최상단에 위치해야 합니다.
st.set_page_config(
    page_title="VoltMaster - 전력 운용 포털", 
    page_icon="⚡", 
    layout="wide"
)

# --- [1단계] robots.txt 자동 생성 로직 ---
# 서버가 실행될 때 파일이 없으면 자동으로 만듭니다.
def ensure_robots_txt():
    if not os.path.exists("static/robots.txt"):
        if not os.path.exists("static"):
            os.makedirs("static")
        with open("static/robots.txt", "w", encoding="utf-8") as f:
            f.write("User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /")

ensure_robots_txt()

# --- [2단계] 애드센스 스크립트 주입 ---
adsense_script = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9577213309229562"
     crossorigin="anonymous"></script>
"""
st.markdown(adsense_script, unsafe_allow_html=True)

# --- [디자인] 사이드바 및 레이아웃 최적화 CSS ---
st.markdown("""
    <style>
        div[data-testid="stSidebarNavViewButton"] { display: none !important; }
        div[data-testid="stSidebarNavSeparator"] { display: none !important; }
        div[data-testid="stSidebarNavItems"] { padding-top: 1rem; }
        .main-title {
            font-size: 3.2rem; 
            color: #FFD700; 
            margin-bottom: 0;
            text-shadow: 2px 2px 4px #000000;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 메인 홈 렌더링 함수
def render_main_home():
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0rem;">
            <h1 class="main-title">⚡ VoltMaster</h1>
            <p style="font-size: 1.2rem; color: #AAAAAA; font-weight: 300;">Data Center Power Infrastructure Engineering Portal</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Core Engineering Tools")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 25px; border-radius: 15px; border-left: 6px solid #FFD700; height: 180px; margin-bottom: 10px;">
                <h2 style="margin:0; color: #FFFFFF;">🧮 1. 실무 전력 계산기</h2>
                <p style="color: #BBBBBB; font-size: 0.95rem; margin-top: 10px;">
                    TR 수량 산정, UPS 부하 계산, 효율 분석 등<br>데이터센터 현장 실무 12개 전문 모듈 통합
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("계산기 엔진 기동 🏎️", use_container_width=True, key="main_calc", type="primary"):
            st.switch_page("pages/1_calculator.py")

    with col2:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 25px; border-radius: 15px; border-left: 6px solid #00BFFF; height: 180px; margin-bottom: 10px;">
                <h2 style="margin:0; color: #FFFFFF;">🤖 2. AI 자격증 튜터</h2>
                <p style="color: #BBBBBB; font-size: 0.95rem; margin-top: 10px;">
                    건축전기기술사 및 전기분야 자격증 학습 지원<br>기출문제 분석 및 실시간 질의응답 가이드
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("AI 튜터와 학습 시작 📚", use_container_width=True, key="main_ai", type="primary"):
            st.switch_page("pages/2_ai_tutor.py")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### 📁 Technical Archive & Trends")
    m_col1, m_col2 = st.columns(2)
    m_col3, m_col4 = st.columns(2)

    with m_col1:
        with st.container(border=True):
            st.subheader("📚 3. 설비 아카이브")
            st.caption("변압기, 발전기, UPS 제작 사양 및 기술 매뉴얼")
            if st.button("아카이브 바로가기", key="go_3", use_container_width=True):
                st.switch_page("pages/3_manuals.py")

    with m_col2:
        with st.container(border=True):
            st.subheader("📝 4. 현장 점검 양식")
            st.caption("체크리스트, 안전 진단 양식 및 보고서 템플릿")
            if st.button("양식함 열기", key="go_4", use_container_width=True):
                st.switch_page("pages/4_templates.py")

    with m_col3:
        with st.container(border=True):
            st.subheader("🔍 5. KEC 스마트 검색기")
            st.caption("한국전기설비규정(KEC) 핵심 조항 고속 검색 및 해석")
            if st.button("KEC 규정 검색", key="go_5", use_container_width=True):
                st.switch_page("pages/5_kec_search.py")

    with m_col4:
        with st.container(border=True):
            st.subheader("☕ 6. 전기인 트렌드")
            st.caption("업계 최신 기술 세미나, 전시회 및 핫플레이스 정보")
            if st.button("최신 트렌드 보기", key="go_6", use_container_width=True):
                st.switch_page("pages/6_blog_events.py")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.write("© 2026 VoltMaster. All rights reserved.")
    with f_col2:
        st.write("Contact: [jiyongna82@gmail.com](mailto:jiyongna82@gmail.com)")

# 4. 내비게이션 설정
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
    ]
}

if st.query_params.get("manage") == "true" or st.session_state.get("is_admin", False):
    st.session_state.is_admin = True
    pages_dict["🔐 시스템 관리"] = [
        st.Page("pages/admin_notice.py", title="공지사항 관리", icon="⚙️")
    ]

# 실행
pg = st.navigation(pages_dict)
pg.run()