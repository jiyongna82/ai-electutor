import streamlit as st

# --- [상단 안내 문구] ---
st.warning("""
⚠️ **안내:** 본 페이지는 **VoltMaster 뉴스레터의 레이아웃 구성을 보여드리기 위한 샘플**입니다. 
실제 발행 시에는 이 틀을 바탕으로 최신 기술 동향과 현장 데이터를 반영하여 작성됩니다.
""")

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# 🔋 VoltMaster Insight: Vol. 03
### **"무정전 전원장치(UPS)의 신뢰성: 축전지 열화 진단과 유지보수 전략"**
---
""")

st.info("""
**[Editor's Message]** 안녕하십니까, **VoltMaster**입니다.  
데이터센터의 '최후의 보루'가 비상발전기라면, 정전 즉시 부하를 책임지는 '0초의 파수꾼'은 바로 UPS입니다. 
최근 리튬 배터리 도입이 늘고 있지만, 여전히 많은 현장에서 쓰이는 납축전지의 관리 소홀은 대형 사고로 이어지곤 합니다. 
이번 3호에서는 축전지 내부저항 측정의 중요성과 UPS 효율 최적화 방안을 다룹니다.
""")

# --- 2. [Deep Dive] 이달의 기술 심층 분석 ---
st.markdown("## 📚 Deep Dive: UPS 및 축전지 공학")
with st.container(border=True):
    st.markdown("### **축전지 열화 판정의 핵심: 내부저항(Internal Resistance)**")
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        축전지는 사용 시간이 경과함에 따라 전극의 부식과 전해액 감소로 인해 **내부저항**이 증가합니다. 
        일반적으로 신품 대비 내부저항이 **1.5~2배 이상** 증가하면 수명이 다한 것으로 판정하며, 
        이는 정전 시 기대했던 백업 시간을 보장하지 못한다는 위험 신호입니다.
        
        기술사 시험에서는 축전지의 용량 산정 식인 $C = \frac{1}{L} \times [K_1I_1 + K_2(I_2 - I_1) + \dots]$를 
        정확히 숙지하고, 온도에 따른 방전 특성 변화를 설계에 어떻게 반영할 것인지 논리적으로 
        기술하는 것이 고득점의 포인트입니다.
        """)
    with col_img:
        # 축전지 내부저항 측정 및 열화 곡선 그래프 이미지
        st.image("https://via.placeholder.com/300x200.png?text=Battery+Impedance+Test", caption="배터리 테스터를 이용한 내부저항 측정")



st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 글로벌 기술 동향 (박스 레이아웃) ---
st.markdown("## 📍 3월 글로벌 전력 기술 트렌드")
st.caption("해외 데이터센터 및 차세대 에너지 저장 기술 소식")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### **Li-ion vs LFP**\n**BESS 배틀**")
        st.markdown("📅 26.03.10")
        img_url = "https://via.placeholder.com/400x200.png?text=LFP+Battery+Tech"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("데이터센터용 LFP 배터리의 안전성 및 경제성 분석 보고서")
        st.link_button("상세보기", "https://www.iea.org/", use_container_width=True)

with c2:
    with st.container(border=True):
        st.markdown("### **고효율 UPS**\n**Eco-Mode 실증**")
        st.markdown("📅 26.03.18")
        img_url = "https://via.placeholder.com/400x200.png?text=UPS+Eco+Mode"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("99% 이상의 효율을 달성하기 위한 UPS 바이패스 운용 최적화")
        st.link_button("상세보기", "https://www.ieee.org/", use_container_width=True)

with c3:
    with st.container(border=True):
        st.markdown("### **수소 연료전지**\n**비상전원 적용**")
        st.markdown("📅 26.03.25")
        img_url = "https://via.placeholder.com/400x200.png?text=Hydrogen+Fuel+Cell"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("친환경 데이터센터를 위한 디젤 발전기 대체 기술 로드맵")
        st.link_button("상세보기", "https://www.energy.gov/", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트 ---
st.markdown("## 🛠️ 실무 꿀팁: UPS실 환경 관리")
with st.expander("✅ 축전지 수명 연장을 위한 3대 환경 조건", expanded=True):
    st.write("""
    1. **온도 관리:** 축전지실 온도를 25℃로 유지하세요. 온도가 10℃ 상승할 때마다 기대 수명은 절반으로 단축됩니다.
    2. **단자 체결력:** 열화상 카메라를 이용하여 배터리 간 연결 단자의 접촉 저항(발열) 여부를 정기적으로 스캔하세요.
    3. **부동 충전 전압:** 각 셀(Cell)당 충전 전압이 제조사 권장치(예: 2.23~2.25V)를 벗어나지 않는지 확인이 필요합니다.
    """)

# --- 5. [Closing] 다음 호 예고 ---
st.divider()
st.markdown("### 📅 Next Issue")
st.write("Vol. 04 예고: **'서버실 냉방 효율의 핵심: 기류 분석(CFD)과 핫에일/콜드에일 차폐 기술'**")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("발행처: VoltMaster Engineering Team | 본 페이지는 샘플 레이아웃입니다.")