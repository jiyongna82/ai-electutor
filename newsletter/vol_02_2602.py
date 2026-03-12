import streamlit as st

# --- [상단 안내 문구] ---
st.warning("""
⚠️ **안내:** 본 페이지는 **VoltMaster 뉴스레터의 레이아웃 구성을 보여드리기 위한 샘플**입니다. 
실제 발행 시에는 이 틀을 바탕으로 최신 기술 동향과 현장 데이터를 반영하여 작성됩니다.
""")

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# 🌡️ VoltMaster Insight: Vol. 02
### **"데이터센터의 심장: 메인 변압기 건전성 진단과 보호 협조"**
---
""")

st.info("""
**[Editor's Message]** 안녕하십니까, **VoltMaster**입니다.  
데이터센터 운영의 안정성은 '끊김 없는 전력 공급'에서 시작됩니다. 특히 수전 설비의 핵심인 특고압 변압기는 
사소한 이상 징후가 대형 사고로 이어질 수 있습니다. 이번 2호에서는 변압기 내부 상태를 과학적으로 판별하는 
**DGA(유중가스 분석)**와 **비율차동계전기**의 역할을 심층 분석합니다.
""")

# --- 2. [Deep Dive] 이달의 기술 심층 분석 ---
st.markdown("## 📚 Deep Dive: 변압기 예방진단")
with st.container(border=True):
    st.markdown("### **유입변압기 내부 이상 진단: 유중가스 분석(DGA)**")
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        특고압 유입변압기는 수천 리터의 절연유를 품고 있습니다. 
        내부에 국부적인 과열이나 아크가 발생하면 절연유가 열분해되며 아세틸렌($C_2H_2$), 수소($H_2$), 메탄($CH_4$) 등의 가스가 발생합니다.
        
        특히 **아세틸렌**이 검출된다면 이는 고온 아크(Arcing)의 강력한 증거이므로 즉시 정밀 진단이 필요합니다. 
        또한, **비율차동계전기(87번)**가 변압기 1, 2차측 CT 전류 차이를 상시 감시하여 내부 고장 시 
        0.1초 이내에 차단기를 개방하도록 설정된 보호 협조 곡선을 이해하는 것이 엔지니어의 핵심 역량입니다.
        """)
    with col_img:
        # 변압기 내부 고장 진단 메커니즘 이미지
        st.image("https://via.placeholder.com/300x200.png?text=Transformer+DGA+Analysis", caption="절연유 가스 분석을 통한 상태 판정")



st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 기술 세미나 및 교육 (박스 레이아웃) ---
st.markdown("## 📍 2월 전기안전 전문 교육")
st.caption("전기안전관리자 및 실무자를 위한 직무교육 일정")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### **특고압 설비**\n**정밀 진단 실무**")
        st.markdown("📅 26.02.11 ~ 02.13")
        img_url = "https://via.placeholder.com/400x200.png?text=Diagnosis+Training"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("초음파 및 부분방전(PD) 진단 기법 실습 및 사례 연구")
        st.link_button("상세보기", "https://www.kesco.or.kr/", use_container_width=True)

with c2:
    with st.container(border=True):
        st.markdown("### **KEC 적용**\n**보호협조 계산**")
        st.markdown("📅 26.02.18")
        img_url = "https://via.placeholder.com/400x200.png?text=KEC+Calculation"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("KEC 규정에 따른 단락용량 계산 및 보호계전기 세팅")
        st.link_button("상세보기", "http://www.kea.kr/", use_container_width=True)

with c3:
    with st.container(border=True):
        st.markdown("### **데이터센터**\n**소방 안전 포럼**")
        st.markdown("📅 26.02.25")
        img_url = "https://via.placeholder.com/400x200.png?text=Safety+Forum"
        st.markdown(f'<div style="width:100%;height:150px;overflow:hidden;border-radius:8px;"><img src="{img_url}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("리튬 배터리 화재 대응 및 가스 소화 설비 연동 최적화")
        st.link_button("상세보기", "https://www.nfa.go.kr/", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트 ---
st.markdown("## 🛠️ 실무 꿀팁: 수배전반 점검")
with st.expander("✅ 유입변압기 외관 및 상태 점검 포인트", expanded=True):
    st.write("""
    1. **방열판 누유 점검:** 변압기 하부 및 밸브 접속부에서 절연유가 배어 나오는지 손전등으로 세밀히 확인하세요.
    2. **다이얼 온도계 체크:** 변압기 유온이 상온 대비 급격히 상승(70℃ 초과)했다면 부하율 및 냉각팬을 점검해야 합니다.
    3. **흡습호흡기 실리카겔:** 실리카겔 색상이 2/3 이상 변했다면 교체하세요. 수분 유입은 절연 파괴의 주원인입니다.
    """)

# --- 5. [Closing] 다음 호 예고 ---
st.divider()
st.markdown("### 📅 Next Issue")
st.write("Vol. 03 예고: **'무정전 전원장치(UPS) 효율 관리와 축전지 열화 진단 기술'**")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("발행처: VoltMaster Engineering Team | 본 페이지는 샘플 레이아웃입니다.")