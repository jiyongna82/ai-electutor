import streamlit as st
import os

# --- 1. 환경 설정 ---
NEWSLETTER_DIR = "newsletter"

# --- 2. 데이터 처리 함수 ---
def get_newsletter_data():
    if not os.path.exists(NEWSLETTER_DIR):
        os.makedirs(NEWSLETTER_DIR)
        return []
    
    files = [f for f in os.listdir(NEWSLETTER_DIR) if f.startswith("vol_") and f.endswith(".py")]
    files.sort(reverse=True) # 최신순 정렬
    
    newsletters = []
    for i, file in enumerate(files):
        try:
            parts = file.split('_')
            vol_num = int(parts[1])
            date_raw = parts[2].replace(".py", "")
            
            year = date_raw[:2]
            month = int(date_raw[2:])
            
            # 기본 레이블: 26년 1월 1호
            label = f"{year}년 {month}월 {vol_num}호"
            
            # [수정] 촌스러운 빨간 공 대신 텍스트로 New 강조
            # 스트림릿 셀렉트박스 특성상 텍스트 조합으로 최신호 표시
            if i == 0:
                label = f"{label} (New)"
            
            newsletters.append({
                "file": file,
                "label": label,
                "vol": vol_num,
                "path": os.path.join(NEWSLETTER_DIR, file)
            })
        except:
            continue
    return newsletters

def render_newsletter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        exec(f.read(), globals())

# --- 3. 레이아웃 설정 ---
st.set_page_config(page_title="인사이트 & 뉴스레터 | VoltMaster", page_icon="🗞️", layout="wide")
news_list = get_newsletter_data()

# 초기값 설정
selected_news = None

# --- 4. 사이드바 (내비게이션) ---
with st.sidebar:
    st.markdown("---")
    st.subheader("📬 뉴스레터 아카이브")
    
    if not news_list:
        st.info("발행된 뉴스레터가 없습니다.")
    else:
        options = [n["label"] for n in news_list]
        selected_label = st.selectbox("회차 선택", options, index=0)
        selected_news = next((n for n in news_list if n["label"] == selected_label), None)

    st.markdown("---")
    st.caption("© 2026 VoltMaster")

# --- 5. 메인 본문 렌더링 ---
if selected_news:
    # [수정] 메인 타이틀에서 New 글씨만 빨간색으로 강조 (HTML 활용)
    display_title = selected_label.replace(" (New)", "")
    
    if "(New)" in selected_label:
        st.markdown(f"### 🗞️ {display_title} <span style='color: #FF4B4B; font-size: 0.8em; font-weight: bold; vertical-align: middle; margin-left: 10px;'>NEW</span>", unsafe_allow_html=True)
    else:
        st.title(f"🗞️ {display_title}")
        
    st.caption(f"VoltMaster 전력 기술 인사이트 - Vol.{selected_news['vol']}")
    st.divider()
    
    try:
        render_newsletter(selected_news["path"])
    except Exception as e:
        st.error(f"뉴스레터를 불러오는 중 오류 발생: {e}")
else:
    st.title("🗞️ VoltMaster 인사이트")
    st.info("`newsletter` 폴더에 `vol_01_2601.py` 형식으로 파일을 추가해 주세요.")

# --- 6. 푸터 ---
st.markdown("<br><br><div style='text-align: center; opacity: 0.5; font-size: 11px; color: gray;'>© 2026 VoltMaster. All rights reserved.</div>", unsafe_allow_html=True)