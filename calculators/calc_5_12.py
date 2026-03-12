import streamlit as st
import time

def run_calc():
    st.subheader("5-12. 데이터센터 PUE 및 에너지 효율 시뮬레이터")
    st.caption("데이터센터의 총 전력 소비량과 IT 부하량을 바탕으로 PUE 지수를 산출하고, 냉방/공조 효율 개선에 따른 전력 절감 효과를 분석합니다.")
    
    # PUE 기본 공식
    st.latex(r"PUE = \frac{Total\ Facility\ Power}{IT\ Equipment\ Power} = \frac{P_{IT} + P_{Cooling} + P_{Loss}}{P_{IT}}")
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.9em;'>(PUE 1.0에 가까울수록 효율적이며, 국내 평균은 약 1.4~1.8 수준입니다.)</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📥 1. 현재 전력 소비 현황")
        it_load_kw = st.number_input("IT 장비 소비전력 (kW)", min_value=1.0, value=1000.0, step=100.0)
        cooling_load_kw = st.number_input("냉방/공조 설비 소비전력 (kW)", min_value=0.0, value=400.0, step=50.0)
        etc_load_kw = st.number_input("기타 설비 및 손실 (조명/UPS손실 등, kW)", min_value=0.0, value=100.0, step=10.0)
        
        st.markdown("---")
        st.subheader("🎯 2. 효율 개선 목표")
        target_pue = st.slider("목표 PUE 지수", 1.1, 1.5, 1.25, step=0.01)

        btn = st.button("에너지 효율 분석 시작 🚀", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 PUE 및 에너지 구조 분석")
        if btn:
            with st.spinner("센터 에너지 프로파일링 중..."):
                time.sleep(0.8)

            # 1. 현재 PUE 계산
            total_power = it_load_kw + cooling_load_kw + etc_load_kw
            current_pue = total_power / it_load_kw
            
            # 2. 목표 PUE 달성을 위한 목표 총 전력 및 냉방 절감량
            target_total_power = it_load_kw * target_pue
            needed_reduction_kw = total_power - target_total_power
            
            # 3. pPUE (Partial PUE - 냉방 부문)
            p_pue_cooling = cooling_load_kw / it_load_kw

            if current_pue <= 1.2:
                status = "최상위 (World Class)"
                color = "green"
            elif current_pue <= 1.5:
                status = "우수 (Advanced)"
                color = "blue"
            else:
                status = "개선 필요 (Standard)"
                color = "orange"

            st.markdown(f"### 현재 PUE: <span style='color:{color}'>{current_pue:.2f}</span> ({status})", unsafe_allow_html=True)

            # 결과 메트릭
            m1, m2 = st.columns(2)
            m1.metric("현재 총 소비전력", f"{total_power:,.0f} kW")
            m1.metric("냉방 부분 pPUE", f"{p_pue_cooling:.2f}")
            
            m2.metric("목표 대비 절감 필요량", f"{needed_reduction_kw:,.1f} kW", delta=f"-{needed_reduction_kw:,.1f} kW", delta_color="normal")
            m2.metric("목표 총 전력량", f"{target_total_power:,.0f} kW")

            st.divider()
            st.info(f"""
            **[데이터센터 운영 전문가 가이드]**
            * **PUE 개선 전략:** 현재 목표 PUE **{target_pue}**를 달성하려면 전체 시스템에서 **{needed_reduction_kw:.1f}kW**의 전력을 더 줄여야 합니다. 
            * **프리쿨링(Free Cooling):** 지용 님 센터의 열교환기를 활용한 프리쿨링 모드 가동 시간을 늘리면 냉방 전력을 획기적으로 낮춰 PUE를 개선할 수 있습니다.
            * **차폐 시스템:** 컨테인먼트(Containment) 설치를 통해 냉복도/핫복도를 분리하면 송풍기 전력을 아껴 PUE를 약 0.1~0.2 포인트 낮출 수 있습니다.
            * **기술사 Tip:** 건축전기설비기술사 제121회 등에서 DC 에너지 효율화 방안으로 PUE와 함께 **WUE(물 사용 효율)**, **CUE(탄소 사용 효율)**가 함께 언급되므로 연계 학습이 필요합니다.
            """)
        else:
            st.info("좌측에 실시간 전력 사용 데이터를 입력하여 PUE를 산출하세요.")