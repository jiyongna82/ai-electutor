import streamlit as st
import time

def run_calc():
    st.subheader("5-11. 태양광 발전 기반 전기요금 세이빙 시뮬레이터")
    st.caption("태양광 설치 용량에 따른 연간 발전량을 예측하고, 이를 통한 전기요금 절감액(기본요금+전력량요금) 및 탄소 저감 효과를 분석합니다.")
    
    # 발전량 및 세이빙 기본 공식
    st.latex(r"E_{year} = P_{pv} \times h_{day} \times 365 \times \eta, \quad Saving = (E_{year} \times Unit) + (P_{peak\_cut} \times Base)")
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.9em;'>(E: 연간발전량, P: 용량, h: 발전시간, η: 효율, Unit: 전력량단가, Base: 기본요금단가)</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📥 1. 태양광 설비 제원")
        pv_cap = st.number_input("태양광 설치 용량 (kWp)", min_value=0.0, value=100.0, step=10.0)
        avg_gen_hour = st.slider("일평균 발전 시간 (hr)", 3.0, 4.5, 3.6, help="국내 평균은 약 3.4~3.8시간 내외입니다.")
        system_eff = st.slider("시스템 종합 효율 (%)", 70.0, 95.0, 85.0, help="인버터 손실, 오염, 온도 계수 등을 포함한 실효율입니다.")

        st.markdown("---")
        st.subheader("💰 2. 요금 절감 변수")
        energy_unit_price = st.number_input("적용 전력량 요금 단가 (원/kWh)", min_value=0, value=150, help="자가소비로 아끼는 평균 단가를 입력하세요.")
        peak_reduction_kw = st.number_input("예상 피크 감소 기여 (kW)", min_value=0.0, value=pv_cap * 0.1, help="태양광 발전을 통한 기본요금 절감 예상치입니다.")
        base_unit_price = st.number_input("기본요금 단가 (원/kW)", min_value=0, value=8320)

        btn = st.button("세이빙 효과 분석 시작 🚀", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 경제성 및 환경 분석 리포트")
        if btn:
            with st.spinner("발전 프로파일 및 요금 체계 시뮬레이션 중..."):
                time.sleep(0.8)

            # 1. 발전량 계산
            daily_gen = pv_cap * avg_gen_hour * (system_eff / 100)
            yearly_gen = daily_gen * 365
            
            # 2. 요금 절감액 계산
            annual_energy_saving = yearly_gen * energy_unit_price
            annual_base_saving = peak_reduction_kw * base_unit_price * 12
            total_saving = annual_energy_saving + annual_base_saving
            
            # 3. 환경 효과 (CO2 저감량)
            co2_reduction = yearly_gen * 0.466 / 1000  # ton CO2

            st.success(f"✅ 연간 약 {total_saving/10000:,.1f}만 원 절감 효과")

            # 결과 메트릭
            m1, m2 = st.columns(2)
            m1.metric("연간 예상 발전량", f"{yearly_gen:,.0f} kWh")
            m1.metric("전력량요금 절감 (연)", f"{annual_energy_saving:,.0f} 원")
            
            m2.metric("탄소 배출 저감량", f"{co2_reduction:.2f} tCO2")
            m2.metric("기본요금 절감 (연)", f"{annual_base_saving:,.0f} 원")

            st.divider()
            st.subheader("💵 총 연간 세이빙액")
            st.title(f"{int(total_saving):,} 원/년")

            st.info(f"""
            **[에너지 경영 전문가 가이드]**
            * **피크 컷(Peak Cut):** 태양광 발전은 전력 수요가 높은 낮 시간대에 집중되므로, 건물 최대 피크를 낮춰 **기본요금 절감**에 큰 도움이 됩니다.
            * **환경적 가치:** 산출된 탄소 저감량(**{co2_reduction:.2f}t**)은 추후 탄소배출권 거래나 RE100 달성 지표로 활용될 수 있습니다.
            * **관리 제언:** 데이터센터 옥상 등 설치 환경에 따라 먼지 등으로 인한 효율 저하가 발생할 수 있으니 주기적인 청소를 권장합니다.
            """)
        else:
            st.info("좌측에 설비 데이터를 입력하여 경제적 가치를 확인하세요.")