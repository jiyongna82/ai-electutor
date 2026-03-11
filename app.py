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

# --- [1단계] 구글 인증 ---
verification_code = "uXxXH_PzU8GwoKbIjxKaFuGOCuYV7EWnk3wr9b9OtrM"
adsense_id = "ca-pub-9577213309229562"
st.markdown(f"""
    <div style="display: none;">
        <meta name="google-adsense-account" content="{adsense_id}">
        <meta name="google-site-verification" content="{verification_code}" />
    </div>
""", unsafe_allow_html=True)

# --- [2단계] 정적 파일 생성 ---
if not os.path.exists("static"): os.makedirs("static")
with open("static/robots.txt", "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /")

# --- [3단계] 디자인: CSS ---
st.markdown("""
    <style>
        /* 기본 네비게이션 스타일링 감추기 */
        div[data-testid="stSidebarNavViewButton"] { display: none !important; }
        div[data-testid="stSidebarNavSeparator"] { display: none !important; }
        
        /* Streamlit 메인 컨테이너 상단 기본 여백 대폭 축소 */
        .block-container {
            padding-top: 2rem !important; 
            padding-bottom: 2rem !important;
        }

        /* 메인 타이틀 강조 */
        .hero-title { 
            font-weight: 900;
            text-align: center; 
            margin-top: 0px;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .hero-title .logo {
            font-size: 5.5rem; 
            vertical-align: middle;
        }
        .hero-title .text-black {
            font-size: 4.5rem;
            color: #000000;
            text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.4); 
            vertical-align: middle;
        }
        .hero-title .text-orange {
            font-size: 4.5rem;
            color: #FF8C00; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            vertical-align: middle;
        }

        .hero-subtitle { 
            font-size: 1.3rem; 
            color: #A0AEC0; 
            text-align: center; 
            letter-spacing: 1px;
            margin-top: 5px;
            margin-bottom: 30px; 
        }
        
        /* 메인 핵심 기능 카드 */
        .core-card {
            background-color: #1E293B; 
            padding: 30px 20px; 
            border-radius: 15px; 
            text-align: center; 
            min-height: 220px; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4); 
            margin-bottom: 15px;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            word-break: keep-all;
        }
        .core-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 8px 15px rgba(0,0,0,0.5);
        }
        
        /* 하단 서브 카드 (마우스 반응 및 그림자 효과 추가) */
        .sub-card {
            background-color: #2D3748; 
            padding: 20px 25px; 
            border-radius: 12px; 
            min-height: 140px; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            margin-bottom: 15px;
            word-break: keep-all;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .sub-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        }
        
        /* 푸터 구분선 및 간격 스타일 */
        hr { margin-top: 3.5rem !important; margin-bottom: 1rem !important; border: 0; border-top: 1px solid #444; }
        div[data-testid="column"] { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- [4단계] 메인 화면 렌더링 함수 ---
def render_main_home():
    # 1. Main 타이틀 (margin-top 제거하여 위로 밀착)
    st.markdown('''
        <div>
            <h1 class="hero-title">
                <span class="logo">⚡</span> 
                <span class="text-black">Volt</span><span class="text-orange">M</span><span class="text-black">aster</span>
            </h1>
            <p class="hero-subtitle">Professional Power Engineering & Management Portal</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # 2. Core Engineering Tools
    st.markdown("### 🚀 Core Engineering Tools")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
            <div class="core-card" style="border-top: 6px solid #FF8C00;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🖥️</div>
                <h3 style="color: #FFFFFF; margin: 0 0 10px 0;">실무 전력 계산기</h3>
                <p style="color: #94A3B8; margin: 0; font-size: 0.95rem; line-height: 1.5;">현장 실무에 최적화된 다양한 전력 분석 및 계산 모듈 제공</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("계산기 엔진 기동 ✈️", use_container_width=True, type="primary", key="btn_calc"): st.switch_page("pages/1_calculator.py")
        
    with col2:
        st.markdown('''
            <div class="core-card" style="border-top: 6px solid #00BFFF;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">✨</div>
                <h3 style="color: #FFFFFF; margin: 0 0 10px 0;">AI 자격증 튜터</h3>
                <p style="color: #94A3B8; margin: 0; font-size: 0.95rem; line-height: 1.5;">건축전기설비기술사 및 국가기술자격증 합격을 위한 맞춤형 AI 학습</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("AI 튜터와 학습 시작 📚", use_container_width=True, type="primary", key="btn_tutor"): st.switch_page("pages/2_ai_tutor.py")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. 부가 기능 및 서비스
    st.markdown("### 📌 부가 서비스 및 커뮤니티")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown('''
            <div class="sub-card" style="border-top: 5px solid #10B981;">
                <h4 style="color: #E2E8F0; margin-top: 0; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">📁 기술 자료실</h4>
                <p style="color: #A0AEC0; font-size: 0.85rem; line-height: 1.4; margin: 0;">각종 전기설비 매뉴얼 및 현장 점검 양식 다운로드</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("**자료실 가기**", use_container_width=True, key="btn_archive"): st.switch_page("pages/3_manuals.py")

    with col4:
        st.markdown('''
            <div class="sub-card" style="border-top: 5px solid #6366F1;">
                <h4 style="color: #E2E8F0; margin-top: 0; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">🔍 스마트 KEC</h4>
                <p style="color: #A0AEC0; font-size: 0.85rem; line-height: 1.4; margin: 0;">현장에서 필요한 한국전기설비규정(KEC) 빠른 조항 검색</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("**KEC 검색하기**", use_container_width=True, key="btn_kec"): st.switch_page("pages/5_kec_search.py")

    with col5:
        st.markdown('''
            <div class="sub-card" style="border-top: 5px solid #F43F5E;">
                <h4 style="color: #E2E8F0; margin-top: 0; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">📢 커뮤니티</h4>
                <p style="color: #A0AEC0; font-size: 0.85rem; line-height: 1.4; margin: 0;">전기인 자유게시판, 기술 트렌드 공유 및 고객 지원</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("**게시판 가기**", use_container_width=True, key="btn_board"): st.switch_page("pages/8_free_board.py")


# --- [5단계] 내비게이션 설정 ---
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