import streamlit as st

# --- [상단 안내 문구] ---
st.warning("""
⚠️ **안내:** 본 페이지는 **VoltMaster 뉴스레터의 레이아웃 구성을 보여드리기 위한 샘플**입니다. 
실제 발행 시에는 이 틀을 바탕으로 최신 기술 동향과 현장 데이터를 반영하여 작성됩니다.
""")

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# 🌬️ VoltMaster Insight: Vol. 04
### **"서버실 기류의 마법: 핫에일/콜드에일 차폐와 PUE 최적화"**
---
""")

st.info("""
**[Editor's Message]** 안녕하십니까, **VoltMaster**입니다.  
데이터센터 전력의 절반 가까이가 '열을 식히는 데' 사용된다는 사실, 알고 계신가요? 
단순히 냉동기를 세게 돌리는 것보다 중요한 것은 **차가운 공기와 뜨거운 공기를 섞이지 않게 분리하는 것**입니다. 
이번 4호에서는 서버실 에너지 효율의 척도인 PUE를 낮추는 기류 제어 기술을 심층 분석합니다.
""")

# --- 2. [Deep Dive] 이달의 기술 심층 분석 ---
st.markdown("## 📚 Deep Dive: 열관리 공학")
with st.container(border=True):
    st.markdown("### **기류 차폐 시스템(Containment)과 CFD 분석의 활용**")
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        서버 랙 사이의 통로를 폐쇄하는 **컨테인먼트(Containment)** 시스템은 냉각 효율을 20% 이상 향상시킵니다. 
        차가운 공기 통로를 막는 **CAC(Cold Aisle Containment)**와 뜨거운 공기를 가두는 **HAC(Hot Aisle Containment)** 중 
        우리 센터의 구조에 맞는 최적의 방식은 무엇일까요?
        
        기술사 답안지에는 전산유체역학(**CFD, Computational Fluid Dynamics**) 분석을 통해 
        서버실 내 '열점(Hot Spot)'을 제거하고, 공급 공기 온도($T_{supply}$)와 환기 온도($T_{return}$)의 
        차이인 $\Delta T$를 최적화하여 냉동기 효율(COP)을 극대화하는 방안을 기술해야 합니다.
        """)
    with col_img:
        # 서버실 기류 분석 CFD 시뮬레이션 이미지
        st.image("https://via.placeholder.com/300x200.png?text=CFD+Airflow+Analysis", caption="서버실 기류 및 온도 분포 CFD 시뮬레이션")



st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 냉각 기술 동향 (박스 레이아웃) ---
st.markdown("## 📍 4월 차세대 냉각 기술 트렌드")
st.caption("공냉식을 넘어 액체 냉각으로 가는 과도기의 기술들")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### **액침냉각**\n**Immersion Cooling**")
        st.markdown("📅 26.04.05")
        img_url = "https://via.placeholder.com/400x200.png?text=Immersion+Cooling+Tech"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("서버를 전용 유액에 담가 냉각하는 초고밀도 랙용 냉각 솔루션")
        st.link_button("상세보기", "https://www.ashrae.org/", use_container_width=True)

with c2:
    with st.container(border=True):
        st.markdown("### **외기냉방**\n**Free Cooling**")
        st.markdown("📅 26.04.12")
        img_url = "https://via.placeholder.com/400x200.png?text=Free+Cooling+System"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("중간기 및 동절기 외부 공기를 활용한 냉동기 가동 최소화 전략")
        st.link_button("상세보기", "http://www.harfko.com/", use_container_width=True)

with c3:
    with st.container(border=True):
        st.markdown("### **폐열 회수**\n**Heat Reuse**")
        st.markdown("📅 26.04.20")
        img_url = "https://via.placeholder.com/400x200.png?text=Data+Center+Heat+Reuse"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("데이터센터 발생 폐열을 인근 지역 난방이나 농장에 공급하는 모델")
        st.link_button("상세보기", "https://koreaenergyshow.energy.or.kr/", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트 ---
st.markdown("## 🛠️ 실무 꿀팁: 서버실 기류 점검")
with st.expander("✅ 냉방 효율을 높이는 사소하지만 확실한 습관", expanded=True):
    st.write("""
    1. **블랭킹 판넬(Blanking Panel):** 서버가 장착되지 않은 빈 공간은 반드시 판넬로 막으세요. 차가운 공기의 단락(Bypass)을 방지합니다.
    2. **케이블 정리:** 랙 뒷면의 복잡한 케이블은 뜨거운 공기의 배출을 방해합니다. 기류 통로를 확보하도록 정리하세요.
    3. **천장 보드 확인:** 서버실 이중 천장 보드가 들떠 있으면 컨테인먼트의 압력이 손실되어 냉각 효율이 급격히 떨어집니다.
    """)

# --- 5. [Closing] 다음 호 예고 ---
st.divider()
st.markdown("### 📅 Next Issue")
st.write("Vol. 05 예고: **'2026 상반기 주요 기술 박람회 총정리: 엔지니어의 필드 트립'**")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("발행처: VoltMaster Engineering Team | 본 페이지는 샘플 레이아웃입니다.")