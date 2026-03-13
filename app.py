import streamlit as st
import streamlit.components.v1 as components 
import os
from datetime import datetime

# --- [1단계] 페이지 설정 ---
st.set_page_config(
    page_title="VoltMaster | 전기실무 계산기 & 건축전기설비기술사 AI 튜터", 
    page_icon="⚡", 
    layout="wide"
)

# --- [2단계] 데이터 정의 (인증 정보) ---
adsense_id = "pub-9577213309229562"
verification_code = "uXxXH_PzU8GwoKbIjxKaFuGOCuYV7EWnk3wr9b9OtrM"
naver_code = "31d4310ce9bc01afed10413a6b901a9c8e32746f"

# --- [3단계] 인증 및 검색 엔진 최적화(SEO/썸네일) 설정 ---

# --- [3단계] 인증 및 검색 엔진 최적화(SEO/썸네일) 설정 ---

# 봇이 가장 정확하게 인식할 수 있는 Raw 이미지 주소입니다.
og_image_url = "https://raw.githubusercontent.com/jiyongna82/ai-electutor/425246aedab9075ccdac14d2cfd007d8819999f6/image/VoltMaster_logo%28O%29.jpg"

st.markdown(f"""
    <head>
        <meta name="naver-site-verification" content="{naver_code}" />
        <meta name="google-site-verification" content="{verification_code}" />
        <meta name="google-adsense-account" content="{adsense_id}" />
        
        <title>VoltMaster | 전기실무 포털 & 기술사 AI 튜터</title>
        <meta name="description" content="현직 데이터센터 전문가가 만든 VoltMaster. 전력 계산기, 건축전기설비기술사 학습, KEC 검색 서비스를 제공합니다." />
        
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://ai-electutor.com/" />
        <meta property="og:title" content="VoltMaster | 전기 엔지니어 전문 포털" />
        <meta property="og:description" content="실무 계산기, AI 자격증 튜터, 기술 자료실까지 한 번에 확인하세요." />
        <meta property="og:image" content="{og_image_url}" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:image" content="{og_image_url}" />
    </head>
""", unsafe_allow_html=True)

# --- [3단계] 수정 및 보강 ---
st.markdown(f"""
    <head>
        <meta name="naver-site-verification" content="{naver_code}" />
        <meta name="google-site-verification" content="{verification_code}" />
        <title>VoltMaster | 전기실무 포털</title>
        <meta property="og:title" content="VoltMaster | 전기 엔지니어 필수 포털" />
        <meta property="og:image" content="{og_image_url}" />
        <meta property="og:description" content="실무 계산기 및 AI 자격증 튜터" />
    </head>
""", unsafe_allow_html=True)

# 봇이 메타 태그를 못 읽을 때를 대비해, 페이지 최상단에 투명하게 이미지를 배치합니다.
st.write(f'<img src="{og_image_url}" style="display:none;">', unsafe_allow_html=True)

# --- [4단계] 수집봇 대응 로직 ---
if st.query_params.get("page") == "robots":
    st.text("User-agent: *\nAllow: /"); st.stop()
elif st.query_params.get("page") == "ads":
    st.text(f"google.com, {adsense_id}, DIRECT, f08c47fec0942fa0"); st.stop()

# --- [5단계] 디자인: CSS 스타일 (1.55.0 우측 메뉴만 제거 및 버튼 강제 가시화) ---
st.markdown("""
    <style>
        /* 1. 기본 배경 및 헤더 투명화 (숨기지 않고 투명하게만) */
        .stApp { background-color: #F8FAFC !important; }
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            border-bottom: none !important;
            z-index: 1 !important; /* 헤더의 우선순위를 낮춤 */
        }

        /* 2. 🔴 우측 상단 메뉴 및 아이콘만 제거 */
        [data-testid="stStatusWidget"], 
        #MainMenu, 
        .st-emotion-cache-zq59db { 
            display: none !important; 
        }

        /* 3. 🟢 사이드바 버튼 강제 시각화 및 위치 이동 */
        /* 버튼을 감싸는 컨테이너를 헤더 위로 끌어올리고 아래로 밀어냄 */
        div[data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 60px !important;  /* 상단에서 60px 아래로 (이 숫자를 조정해 보세요) */
            left: 15px !important;
            z-index: 999999 !important; /* 최상단 레이어로 설정 */
            background-color: #E67E22 !important; /* 주황색 배경 */
            border-radius: 8px !important;
            padding: 5px !important;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
            display: flex !important;
            visibility: visible !important; /* 강제로 보이게 설정 */
        }

        /* 버튼 아이콘 흰색으로 강조 */
        div[data-testid="stSidebarCollapsedControl"] button svg {
            fill: white !important;
            width: 25px !important;
            height: 25px !important;
        }

        /* 메인 콘텐츠 상단 여백 보정 */
        .block-container {
            padding-top: 4rem !important; 
        }
        
        div[data-testid="stSidebarNavViewButton"] { display: none !important; }
        div[data-testid="stSidebarNavSeparator"] { display: none !important; }
        
        /* 메인 상단 타이틀 스타일 */
        .hero-container { text-align: center; padding: 10px 0 15px 0 !important; }
        .hero-title { font-weight: 900; line-height: 1.1; margin-bottom: 8px !important; }
        .hero-title .text-dark { font-size: 3.8rem; color: #1E293B !important; }
        .hero-title .text-orange { font-size: 3.8rem; color: #E67E22 !important; }
        .hero-subtitle { font-size: 1.1rem; color: #64748B !important; font-weight: 600; }
        
        /* 섹션 및 카드 스타일 */
        .section-header { font-size: 1.5rem !important; font-weight: 800; color: #1E293B !important; margin: 20px 0 10px 0 !important; padding-left: 10px; border-left: 5px solid #E67E22; }
        .card-anchor { text-decoration: none !important; color: inherit !important; display: block; margin-bottom: 10px; }
        .clickable-card { background-color: #FFFFFF !important; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.08); border-radius: 12px; border: 1px solid #E2E8F0; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .clickable-card:hover { transform: translateY(-4px); background-color: #F1F5F9 !important; border: 1px solid #E67E22 !important; }
        .core-box { padding: 25px 20px; min-height: 200px; }
        .sub-box { padding: 20px 15px; min-height: 150px; text-align: center; }
        .card-title-main { font-size: 1.6rem !important; font-weight: 800; color: #0F172A !important; }
        .card-title-sub { font-size: 1.1rem !important; font-weight: 700; color: #0F172A !important; }
        .card-text { color: #475569 !important; font-size: 0.9rem; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- [6단계] 메인 화면 렌더링 함수 ---
def render_main_home():
    st.markdown('''
        <div class="hero-container">
            <h1 class="hero-title">
                <span style="font-size:3.5rem; vertical-align: middle;">⚡</span> 
                <span class="text-dark">Volt</span><span class="text-orange">M</span><span class="text-dark">aster</span>
            </h1>
            <p class="hero-subtitle">Professional Power Engineering & Management Portal</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p class="section-header">🚀 Core Engineering Tools</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            <a href="/calculator" target="_self" class="card-anchor">
                <div class="clickable-card core-box" style="border-top: 6px solid #E67E22;">
                    <div style="font-size: 2.8rem; margin-bottom: 8px;">🖥️</div>
                    <div class="card-title-main">실무 전력 계산기</div>
                    <div class="card-text">부하 계산, 전압강하 등 현장 필수 모듈</div>
                </div>
            </a>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <a href="/ai_tutor" target="_self" class="card-anchor">
                <div class="clickable-card core-box" style="border-top: 6px solid #3498DB;">
                    <div style="font-size: 2.8rem; margin-bottom: 8px;">✨</div>
                    <div class="card-title-main">AI 자격증 튜터</div>
                    <div class="card-text">건축전기설비기술사 등 맞춤형 AI 학습 멘토</div>
                </div>
            </a>
        ''', unsafe_allow_html=True)

    st.markdown('<p class="section-header">📌 부가 서비스 및 커뮤니티</p>', unsafe_allow_html=True)
    
    col3, col4, col5, col6 = st.columns(4)
    services = [
        ("📁", "기술 자료실", "manuals", "#27AE60", "운용 매뉴얼 및 점검 양식 자료"),
        ("🔍", "스마트 KEC", "kec_search", "#2980B9", "KEC 핵심 조항 요약 검색"),
        ("📰", "전기 뉴스레터", "blog_events", "#F39C12", "최신 기술 트렌드 리포트"),
        ("📢", "커뮤니티", "free_board", "#C0392B", "전기인 정보 공유 및 Q&A")
    ]
    cols = [col3, col4, col5, col6]
    for i, (emoji, title, path, color, desc) in enumerate(services):
        with cols[i]:
            st.markdown(f'''
                <a href="/{path}" target="_self" class="card-anchor">
                    <div class="clickable-card sub-box" style="border-top: 5px solid {color};">
                        <div style="font-size: 1.8rem; margin-bottom: 6px;">{emoji}</div>
                        <div class="card-title-sub">{title}</div>
                        <div class="card-text" style="font-size: 0.8rem;">{desc}</div>
                    </div>
                </a>
            ''', unsafe_allow_html=True)

# --- [7단계] 내비게이션 정의 ---
pages_dict = {
    "": [
        st.Page(render_main_home, title="⚡ VoltMaster 홈", default=True), 
        st.Page("pages/1_calculator.py", title="🖥️ 실무 전력 계산기", url_path="calculator")
    ],
    "✨ AI 자격증 튜터": [
        st.Page("pages/2_ai_tutor.py", title="✨ AI 튜터 메인", url_path="ai_tutor"),
        st.Page("tutor/1_professional.py", title="📜 건축전기설비기술사", url_path="professional"),
        st.Page("tutor/2_engineer.py", title="💡 전기기사", url_path="engineer"),
        st.Page("tutor/3_industrial.py", title="🔌 전기산업기사", url_path="industrial"),
        st.Page("tutor/4_craftsman.py", title="🧑‍🔧 전기기능사", url_path="craftsman")
    ],
    "📁 자료 및 정보": [
        st.Page("pages/3_manuals.py", title="📚 설비 아카이브", url_path="manuals"),
        st.Page("pages/4_templates.py", title="📝 현장 점검 양식", url_path="templates"),
        st.Page("pages/5_kec_search.py", title="🔍 KEC 스마트 검색기", url_path="kec_search"),
        st.Page("pages/6_blog_events.py", title="📰 전기 뉴스레터", url_path="blog_events")
    ],
    "📢 소통 및 지원": [
        st.Page("pages/8_free_board.py", title="💬 자유게시판", url_path="free_board"),
        st.Page("pages/0_privacy_policy.py", title="📃 개인정보 처리방침", url_path="privacy_policy")
    ]
}

# --- [8단계] 실행 및 공통 푸터 ---
pg = st.navigation(pages_dict)
pg.run()

# --- [9단계] 공통 푸터 ---
st.divider()
_, footer_col = st.columns([5, 5])
with footer_col:
    st.markdown('''
        <div style="text-align: right; line-height: 1.6; font-size: 0.85rem; color: #475569; padding-right: 10px; padding-bottom: 10px;">
            <p style="margin: 0;">© 2026 <b>VoltMaster. All rights reserved.</b></p>
            <p style="margin: 3px 0;"><a href="/privacy_policy" target="_self" style="text-decoration: none; color: #3498DB; font-weight: bold;">개인정보 처리방침 및 약관</a></p>
            <p style="margin: 0;">Contact: <a href="mailto:jiyong-na@naver.com" style="text-decoration: none; color: #475569;">jiyong-na@naver.com</a></p>
            <p style="margin-top: 3px; font-weight: bold; color: #64748B;">VoltMaster 운영팀</p>
        </div>
    ''', unsafe_allow_html=True)