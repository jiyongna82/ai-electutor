import streamlit as st

# --- [상단 안내 문구] ---
st.warning("""
⚠️ **안내:** 본 페이지는 **VoltMaster 뉴스레터의 레이아웃 구성을 보여드리기 위한 샘플**입니다. 
실제 발행 시에는 이 틀을 바탕으로 최신 기술 동향과 현장 데이터를 반영하여 작성됩니다.
""")

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# ❄️ VoltMaster Insight: Vol. 01
### **"혹한기 데이터센터 전력 설비: 비상발전기 신뢰성 확보 전략"**
---
""")

st.info("""
**[Editor's Message]** 2026년 새해 첫 인사드립니다. **VoltMaster**입니다.  
최근 영하 10도를 밑도는 강추위가 이어지면서 데이터센터의 최후 보루인 '비상발전기' 관리에 비상이 걸렸습니다. 
이번 1호에서는 동절기 시운전 시 주의사항과 냉각수 히터 관리 요령을 집중적으로 다룹니다.
""")

# --- 2. [Deep Dive] 이달의 기술 심층 분석 ---
st.markdown("## 📚 Deep Dive: 전력 계통의 심장")
with st.container(border=True):
    st.markdown("### **DCC급 대용량 발전기의 병렬 운전 및 부하 분담**")
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        데이터센터용 대용량 발전기는 신뢰성 확보를 위해 다수의 유닛을 병렬로 구성합니다. 
        동절기 저온 기동 시에는 엔진 오일 점도가 높아져 초기 윤활에 부하가 걸릴 수 있으므로, 
        **Jacket Water Heater**가 상시 40~50°C를 유지하는지 반드시 모니터링해야 합니다. 
        
        병렬 운전 시 일정 대수 이상의 기동 확립이 확인되어야 메인 VCB가 투입되는 시퀀스 로직을 
        다시 한번 점검하고, 무부하 시운전보다는 실제 부하 투입 시의 전압 및 주파수 변동 폭을 
        확인하여 속도 제어기(Governor)의 응답 특성을 평가하는 것이 핵심입니다.
        """)
    with col_img:
        # 비상발전기 제어 시스템 및 엔진 레이아웃 이미지
        st.image("https://via.placeholder.com/300x200.png?text=Generator+Control+System", caption="발전기 병렬 운전 제어 모니터링")



st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 주요 기술 컨퍼런스 (박스 레이아웃) ---
st.markdown("## 📍 1월 주요 기술 컨퍼런스")
st.caption("새해를 여는 에너지 및 전력 IT 세미나 정보")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### **CES 2026**\n**Energy Tech**")
        st.markdown("📅 26.01.07 ~ 01.10")
        img_url = "https://via.placeholder.com/400x200.png?text=CES+2026+Energy"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("차세대 LFP 배터리 및 전력 솔루션 공개")
        st.link_button("상세보기", "https://www.ces.tech/", use_container_width=True)

with c2:
    with st.container(border=True):
        st.markdown("### **전력계통**\n**동계 안전 세미나**")
        st.markdown("📅 26.01.15")
        img_url = "https://via.placeholder.com/400x200.png?text=Safety+Seminar"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("폭설 및 한파 대비 수배전반 결로 방지 기술 공유")
        st.link_button("상세보기", "http://www.kea.kr/", use_container_width=True)

with c3:
    with st.container(border=True):
        st.markdown("### **AI 데이터센터**\n**전력 포럼**")
        st.markdown("📅 26.01.22")
        img_url = "https://via.placeholder.com/400x200.png?text=AI+DC+Forum"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("초거대 AI 모델 수용을 위한 수전 용량 설계 방안")
        st.link_button("상세보기", "https://koreaenergyshow.energy.or.kr/", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트 ---
st.markdown("## 🛠️ 실무 꿀팁: 동절기 필수 점검")
with st.expander("✅ 영하 10도 이하 시 비상발전기 관리 요령", expanded=True):
    st.write("""
    1. **히터 전원 확인:** Jacket Water Heater 조작반의 전류값을 체크하여 히터 단선 여부를 확인하세요.
    2. **배터리 전압 점검:** 저온에서는 배터리 방전 성능이 20% 이상 저하됩니다. 부동 충전 전압을 상시 체크하세요.
    3. **연료 필터 결빙 방지:** 수분이 포함된 경유는 필터를 막을 수 있습니다. 유수분 분리기를 드레인 하세요.
    """)

# --- 5. [Closing] 다음 호 예고 ---
st.divider()
st.markdown("### 📅 Next Issue")
st.write("Vol. 02 예고: **'변압기 유중가스 분석(DGA)을 통한 내부 이상 진단'**")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("발행처: VoltMaster Engineering Team | 본 페이지는 샘플 레이아웃입니다.")