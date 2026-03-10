import streamlit as st
from comments_tool import render_board  # 분리된 게시판 모듈 불러오기

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# ⚡ VoltMaster Insight: Vol. 05
### **"2026 전력망의 대전환: AI 데이터센터와 차세대 에너지 솔루션"**
---
""")

st.info("""
**[Editor's Message]** 반갑습니다. 전력 계통의 안정과 혁신을 지향하는 **VoltMaster**입니다.  
최근 기온 변화가 심해지면서 센터 내 냉각탑 수위 제어와 비상발전기 히터 점검에 집중하고 있는 요즘입니다. 
이번 5호에서는 기술사 공부의 핵심인 NGR 설계 원리와 상반기 주요 기술 전시회 소식을 함께 담았습니다.
""")

# --- 2. [Deep Dive] 이달의 기술 심층 분석 ---
st.markdown("## 📚 Deep Dive: 전력 계통의 핵심")
with st.container(border=True):
    st.markdown("### **변압기 중성점 접지(NGR)와 지락전류 제한 설계**")
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        우리 센터는 메인 TR 2차측 중성선에 **38.1Ω의 NGR**을 설치하여 지락전류를 **100A 이하**로 제한하고 있습니다. 
        이 수치는 단순한 숫자가 아닙니다. 통신선 유도장해 방지와 기기 손상 억제, 그리고 지락 사고 시에도 시스템의 연속성을 
        확보하기 위한 공학적 설계의 결과입니다. 
        
        기술사 답안지에는 이 '100A'가 갖는 물리적 의미와 보호계전기(OCGR)와의 협조 곡선을 반드시 함께 서술해야 합니다.
        """)
    with col_img:
        # 
        st.image("https://via.placeholder.com/200x150.png?text=NGR+Diagram", caption="NGR 설치 및 지락전류 흐름도")

st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 주요 전시회 & 박람회 정보 ---
st.markdown("## 📍 주요 전시회 & 박람회 정보")
st.caption("2026년 상반기, 전력 및 데이터센터 엔지니어를 위한 핵심 기술 이벤트 큐레이션")

col1, col2, col3 = st.columns(3)

# [박스 1: EPTK]
with col1:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/2992/2992143.png") 
        with head_col2: st.markdown("### **EPTK 2026**\n**국제 전기전력 전시회**")
        st.markdown("📅 **2026. 05. 06 ~ 05. 08**\n📍 **서울 COEX C홀**")
        img_url1 = "https://electrickorea.org/wp-content/uploads/2025/09/01_img01-2.jpg"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url1}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 디지털 보호계전기(IED)\n* 부분방전(PD) 진단\n* KEC 대응 보호협조")
        st.link_button("상세 보기", "http://www.electrickorea.org/", use_container_width=True)

# [박스 2: HARFKO]
with col2:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/11100/11100067.png")
        with head_col2: st.markdown("### **HARFKO 2026**\n**한국국제냉난방공조전**")
        st.markdown("📅 **2026. 10. 21 ~ 10. 23**\n📍 **일산 KINTEX 제1장**")
        img_url2 = "https://www.harfko.com/file_upload/assets/img/exhibit_img/2022/2022_photo11.jpg"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url2}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 무급유 터보냉동기\n* 액침냉각(DTC) 실증\n* 폐열 회수 시스템")
        st.link_button("상세 보기", "http://www.harfko.com/", use_container_width=True)

# [박스 3: 에너지대전]
with col3:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/427/427735.png")
        with head_col2: st.markdown("### **2026 대한민국\n에너지대전**")
        st.markdown("📅 **2026. 09. 16 ~ 09. 18**\n📍 **부산 BEXCO**")
        img_url3 = "https://koreaenergyshow.energy.or.kr/display.do?name=%ea%b5%ad%eb%ac%b4%ec%b4%9d%eb%a6%ac%eb%8b%98+%ec%88%9c%eb%9e%8c(6).JPG&folder=202509&dir_folder=board_gallery"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url3}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 고효율 ICT 솔루션\n* 데이터센터 ESS 연계\n* 분산에너지 활성화")
        st.link_button("상세 보기", "https://koreaenergyshow.energy.or.kr/main/main.do", use_container_width=True)

# [안내 문구]
st.markdown("""
    <div style="background-color: #f8f9fa; border-left: 5px solid #FF4B4B; padding: 15px; border-radius: 5px; margin-top: 10px;">
        <p style="margin: 0; color: #555555; font-size: 0.9em;">
            💡 <b>안내:</b> 일정과 장소는 주최측 사정에 따라 변동될 수 있습니다. 참석 전 공식 홈페이지 확인을 권장드립니다.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트 ---
st.markdown("## 🛠️ 실무 꿀팁: 현장의 소리")
with st.expander("✅ 이번 주 점검 포인트: 고압 부스덕트 절연 관리", expanded=True):
    st.write("""
    - **육안 점검:** 접속부 볼트 캡의 변색 유무를 확인하세요 (과열 징후).
    - **환경 관리:** 결로 방지를 위해 히터가 정상 동작하는지 확인이 필요합니다.
    - **온도 모니터링:** 평소보다 온도가 5℃ 이상 상승했다면 즉시 정밀 진단을 권장합니다.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. [Interactive Board] 게시판 도구 호출 ---
# comments_tool.py 모듈을 사용하여 게시판을 렌더링합니다.
# 닉네임/의견 placeholder와 관리자 삭제 기능이 내장되어 있습니다.
render_board("vol_05")

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. [Closing] Q&A 및 푸터 ---
st.divider()
col_qa, col_info = st.columns(2)
with col_qa:
    st.markdown("### 💬 Q&A")
    st.caption("Q: 터보냉동기 프리쿨링 전환 시점은 언제인가요?")
    st.write("A: 외기 온도가 냉수 환수 온도보다 2~3℃ 낮아지는 늦가을부터가 적기입니다.")
with col_info:
    st.markdown("### 📅 Next Issue")
    st.write("Vol. 06 예고: **'UPS 배터리 수명 예측과 교체 주기'**")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("발행처: VoltMaster Engineering Team | 콘텐츠 문의: [문의하기]")