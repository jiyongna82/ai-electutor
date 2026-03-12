import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime

# --- [1단계] 정적 파일 생성 및 경로 설정 ---
if not os.path.exists("static"): 
    os.makedirs("static")

adsense_id = "ca-pub-9577213309229562"
verification_code = "uXxXH_PzU8GwoKbIjxKaFuGOCuYV7EWnk3wr9b9OtrM"
current_date = datetime.now().strftime("%Y-%m-%d")

robots_content = "User-agent: *\nAllow: /\nSitemap: https://ai-electutor.com/sitemap.xml\n\nUser-agent: Mediapartners-Google\nAllow: /"

sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://ai-electutor.com/</loc><lastmod>{current_date}</lastmod><priority>1.0</priority></url>
    <url><loc>https://ai-electutor.com/calculator</loc><lastmod>{current_date}</lastmod><priority>0.8</priority></url>
    <url><loc>https://ai-electutor.com/ai_tutor</loc><lastmod>{current_date}</lastmod><priority>0.8</priority></url>
    <url><loc>https://ai-electutor.com/manuals</loc><lastmod>{current_date}</lastmod><priority>0.7</priority></url>
    <url><loc>https://ai-electutor.com/templates</loc><lastmod>{current_date}</lastmod><priority>0.7</priority></url>
    <url><loc>https://ai-electutor.com/kec_search</loc><lastmod>{current_date}</lastmod><priority>0.7</priority></url>
    <url><loc>https://ai-electutor.com/free_board</loc><lastmod>{current_date}</lastmod><priority>0.6</priority></url>
    <url><loc>https://ai-electutor.com/privacy_policy</loc><lastmod>{current_date}</lastmod><priority>0.3</priority></url>
</urlset>"""

with open("static/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)
with open("static/ads.txt", "w", encoding="utf-8") as f:
    f.write(f"google.com, {adsense_id}, DIRECT, f08c47fec0942fa0")
with open("static/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

# --- [2단계] 가상 파일 응답 로직 ---
query_page = st.query_params.get("page")
if query_page == "robots":
    st.text(robots_content); st.stop()
elif query_page == "ads":
    st.text(f"google.com, {adsense_id}, DIRECT, f08c47fec0942fa0"); st.stop()
elif query_page == "sitemap":
    st.code(sitemap_xml, language="xml"); st.stop()
elif query_page == "googleac826ba707a1db10":
    st.write("google-site-verification: googleac826ba707a1db10.html"); st.stop()

# --- [3단계] 페이지 설정 및 인증 스크립트 ---
st.set_page_config(page_title="VoltMaster - 전력 운용 포털", page_icon="⚡", layout="wide")
st.markdown(f"""
    <script>
        var meta1 = document.createElement('meta');
        meta1.name = "google-adsense-account"; meta1.content = "{adsense_id}";
        document.getElementsByTagName('head')[0].appendChild(meta1);
        var meta2 = document.createElement('meta');
        meta2.name = "google-site-verification"; meta2.content = "{verification_code}";
        document.getElementsByTagName('head')[0].appendChild(meta2);
    </script>
""", unsafe_allow_html=True)

# --- [4단계] 디자인: CSS (타이틀 크기 대폭 강화) ---
st.markdown("""
    <style>
        div[data-testid="stSidebarNavViewButton"] { display: none !important; }
        div[data-testid="stSidebarNavSeparator"] { display: none !important; }
        .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
        
        /* 메인 타이틀 */
        .hero-title { font-weight: 900; text-align: center; margin-bottom: 0px; }
        .hero-title .text-black { font-size: 4.5rem; color: #1A202C !important; }
        .hero-title .text-orange { font-size: 4.5rem; color: #FF8C00 !important; }
        
        /* 카드 공통 스타일 */
        .core-card, .sub-card {
            color: #FFFFFF !important;
            transition: transform 0.2s;
            word-break: keep-all;
        }
        .core-card {
            background-color: #1E293B; padding: 30px 20px; border-radius: 15px; 
            text-align: center; min-height: 240px; display: flex; flex-direction: column;
            justify-content: center; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.4); 
            margin-bottom: 15px;
        }
        .sub-card {
            background-color: #2D3748; padding: 25px 30px; border-radius: 12px; 
            min-height: 160px; display: flex; flex-direction: column; justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); margin-bottom: 15px;
        }
        .core-card:hover, .sub-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.5); }
        
        /* 카드 내 타이틀 스타일 강화 (크기 업그레이드) */
        .card-title-main { color: #FFFFFF !important; font-size: 1.8rem !important; font-weight: 800 !important; margin-bottom: 15px; }
        .card-title-sub { color: #FFFFFF !important; font-size: 1.5rem !important; font-weight: 700 !important; margin-bottom: 12px; }
        
        /* 카드 내 본문 텍스트 */
        .card-text { color: #CBD5E0 !important; font-size: 1.0rem !important; line-height: 1.5; }

        hr { border-top: 1px solid #444; }
    </style>
""", unsafe_allow_html=True)

# --- [5단계] 메인 화면 렌더링 함수 ---
def render_main_home():
    st.markdown('''
        <div style="text-align:center;">
            <h1 class="hero-title">
                <span style="font-size:5.5rem;">⚡</span> 
                <span class="text-black">Volt</span><span class="text-orange">M</span><span class="text-black">aster</span>
            </h1>
            <p style="font-size:1.3rem; color:#A0AEC0; margin-bottom:30px;">Professional Power Engineering & Management Portal</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Core Engineering Tools")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''<div class="core-card" style="border-top: 6px solid #FF8C00;">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">🖥️</div>
            <div class="card-title-main">실무 전력 계산기</div>
            <div class="card-text">현장 실무에 최적화된 다양한 전력 분석 및 계산 모듈 제공</div></div>''', unsafe_allow_html=True)
        if st.button("계산기 엔진 기동 ✈️", use_container_width=True, type="primary", key="btn_calc"): st.switch_page("pages/1_calculator.py")
    with col2:
        st.markdown('''<div class="core-card" style="border-top: 6px solid #00BFFF;">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">✨</div>
            <div class="card-title-main">AI 자격증 튜터</div>
            <div class="card-text">건축전기설비기술사 및 국가기술자격증 합격을 위한 맞춤형 AI 학습</div></div>''', unsafe_allow_html=True)
        if st.button("AI 튜터와 학습 시작 📚", use_container_width=True, type="primary", key="btn_tutor"): st.switch_page("pages/2_ai_tutor.py")

    st.markdown("### 📌 부가 서비스 및 커뮤니티")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown('''<div class="sub-card" style="border-top: 5px solid #10B981;">
            <div class="card-title-sub">📁 기술 자료실</div>
            <div class="card-text">전기설비 매뉴얼 및 현장 점검 양식 다운로드</div></div>''', unsafe_allow_html=True)
        if st.button("**자료실 가기**", use_container_width=True, key="btn_archive"): st.switch_page("pages/3_manuals.py")
    with col4:
        st.markdown('''<div class="sub-card" style="border-top: 5px solid #6366F1;">
            <div class="card-title-sub">🔍 스마트 KEC</div>
            <div class="card-text">한국전기설비규정(KEC) 빠른 조항 검색</div></div>''', unsafe_allow_html=True)
        if st.button("**KEC 검색하기**", use_container_width=True, key="btn_kec"): st.switch_page("pages/5_kec_search.py")
    with col5:
        st.markdown('''<div class="sub-card" style="border-top: 5px solid #F43F5E;">
            <div class="card-title-sub">📢 커뮤니티</div>
            <div class="card-text">전기인 자유게시판 및 기술 트렌드 공유</div></div>''', unsafe_allow_html=True)
        if st.button("**게시판 가기**", use_container_width=True, key="btn_board"): st.switch_page("pages/8_free_board.py")

# --- [6단계] 내비게이션 및 실행 ---
pages_dict = {
    "": [st.Page(render_main_home, title="⚡ VoltMaster 홈", default=True), st.Page("pages/1_calculator.py", title="🧮 실무 전력 계산기")],
    "✨ AI 자격증 튜터": [st.Page("pages/2_ai_tutor.py", title="✨ AI 튜터 메인/통계"), st.Page("tutor/1_professional.py", title="🥇 건축전기설비기술사"), st.Page("tutor/2_engineer.py", title="🥈 전기기사"), st.Page("tutor/3_industrial.py", title="🥉 전기산업기사"), st.Page("tutor/4_craftsman.py", title="🎖️ 전기기능사")],
    "📁 자료 및 정보": [st.Page("pages/3_manuals.py", title="📚 설비 아카이브"), st.Page("pages/4_templates.py", title="📝 현장 점검 양식"), st.Page("pages/5_kec_search.py", title="🔍 KEC 스마트 검색기"), st.Page("pages/6_blog_events.py", title="☕ 전기인의 핫플 & 트렌드")],
    "📢 소통 및 지원": [st.Page("pages/7_notice.py", title="🔔 공지사항"), st.Page("pages/8_free_board.py", title="💬 자유게시판"), st.Page("pages/9_request_board.py", title="💡 기능/자료 요청"), st.Page("pages/10_contact.py", title="📧 문의하기"), st.Page("pages/0_privacy_policy.py", title="📃 개인정보 처리방침 및 약관")]
}

if st.query_params.get("manage") == "true" or st.session_state.get("is_admin", False):
    st.session_state.is_admin = True
    pages_dict["🔐 시스템 관리"] = [st.Page("pages/admin_notice.py", title="공지사항 관리", icon="⚙️")]

pg = st.navigation(pages_dict)
pg.run()

# --- [7단계] 공통 푸터 ---
st.divider()
_, footer_col = st.columns([5, 5])
with footer_col:
    st.markdown('''
        <div style="text-align: right; line-height: 1.6; font-size: 0.85rem; color: #888; padding-right: 10px;">
            <p style="margin: 0;">© 2026 <b>VoltMaster. All rights reserved.</b></p>
            <p style="margin: 5px 0;"><a href="/privacy_policy" target="_self" style="text-decoration: none; color: #4A90E2; font-weight: bold;">개인정보 처리방침 및 약관</a></p>
            <p style="margin: 0;">Contact: <a href="mailto:jiyong-na@naver.com" style="text-decoration: none; color: #888;">jiyong-na@naver.com</a></p>
            <p style="margin-top: 5px; font-weight: bold; color: #aaa;">VoltMaster 운영팀</p>
        </div>
    ''', unsafe_allow_html=True)