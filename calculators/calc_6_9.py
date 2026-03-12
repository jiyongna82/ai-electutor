import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🌍 6-9. 24/7 무탄소 에너지(CFE) 및 탄소 발자국 분석")
    st.caption("실시간 전력 부하와 선택된 무탄소 에너지원(CFE)을 매칭하여 탄소 중립 이행력을 정밀 분석합니다.")

    # --- 24/7 CFE 및 탄소 발자국 기술 가이드 ---
    with st.expander("📘 24/7 무탄소 에너지(CFE) & 탄소 발자국이란?", expanded=False):
        st.markdown("""
        **1. 24/7 CFE (Carbon-Free Energy)**
        * **정의**: 전력을 사용하는 **그 시점(Hourly Matching)**에 무탄소 에너지원을 실시간으로 매칭하는 방식입니다.
        * **운영**: 태양광이 없는 야간이나 풍력이 멈춘 시간에도 원자력, 수소, ESS 등을 통해 탄소 없는 전기를 써야 함을 의미합니다.

        **2. 실시간 탄소 발자국 (Carbon Footprint)**
        * **계산 방식**: 총 전력량 중 무탄소 전원으로 충당하지 못한 **나머지 한전 전력량(Grid)**에 해당 지역의 탄소 집약도(gCO2/kWh)를 곱하여 산출합니다.
        """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 센터 총 부하 설정")
        total_load = st.number_input("현재 센터 총 IT/시설 부하 (kW)", value=2500, step=100)
        
        st.markdown("---")
        st.markdown("#### 🌱 2. 무탄소 에너지원(CFE) 선택")
        st.info("현재 공급 중인 에너지원을 체크하면 계산에 자동으로 반영됩니다.")

        cfe_sources = []
        
        # 체크박스 기반의 동적 에너지원 입력
        if st.checkbox("자가용 태양광 (On-site PV)", value=True):
            pv_gen = st.number_input("태양광 발전량 (kW)", value=250, step=10, key="pv_6_9")
            cfe_sources.append({"에너지원": "태양광", "공급량(kW)": pv_gen})

        if st.checkbox("외부 재생에너지 PPA", value=False):
            ppa_gen = st.number_input("PPA 수전량 (kW)", value=500, step=50, key="ppa_6_9")
            cfe_sources.append({"에너지원": "PPA 재생", "공급량(kW)": ppa_gen})

        if st.checkbox("수소 연료전지 (Fuel Cell)", value=False):
            fc_gen = st.number_input("연료전지 출력 (kW)", value=100, step=10, key="fc_6_9")
            cfe_sources.append({"에너지원": "연료전지", "공급량(kW)": fc_gen})

        if st.checkbox("무탄소 그리드 수전 (Nuclear/Hydro)", value=False):
            grid_cfe = st.number_input("CFE 인증 수전량 (kW)", value=1000, step=100, key="grid_cfe_6_9")
            cfe_sources.append({"에너지원": "그리드CFE", "공급량(kW)": grid_cfe})

        st.markdown("---")
        grid_intensity = st.slider("현재 그리드 탄소 집약도 (gCO2/kWh)", 100, 800, 450)

        btn = st.button("실시간 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 실시간 전력 수급 및 CFE 리포트")
        if btn:
            # --- 계산 로직 ---
            total_cfe_supply = sum(item['공급량(kW)'] for item in cfe_sources)
            # 한전 전력량 (Grid) = 총 부하 - 무탄소 전원 공급량
            net_grid_pwr = max(0, total_load - total_cfe_supply)
            
            # CFE Score 산출
            cfe_score = min(100.0, (total_cfe_supply / total_load * 100)) if total_load > 0 else 0
            
            # 탄소 발자국 계산
            carbon_emission = (net_grid_pwr * grid_intensity) / 1000 # kgCO2/h

            # --- 결과 시각화 (요청사항 반영) ---
            c1, c2 = st.columns(2)
            c1.metric("센터 총 소비 부하", f"{total_load:,} kW")
            c2.metric("실시간 한전 전력", f"{net_grid_pwr:,} kW", delta="Grid Supply", delta_color="inverse")

            st.markdown("---")
            # 상세 에너지원 구성
            if cfe_sources:
                st.dataframe(pd.DataFrame(cfe_sources), use_container_width=True, hide_index=True)
            else:
                st.warning("선택된 무탄소 전원이 없습니다. 현재 100% 한전 전력을 사용 중입니다.")

            st.metric("실시간 CFE 매칭률 (CFE Score)", f"{cfe_score:.1f} %", 
                      delta=f"{total_cfe_supply:,} kW CFE 확보")

            st.markdown(f"##### 💡 실시간 탄소 발자국: **{carbon_emission:.2f} kgCO2/h**")
            
            if cfe_score >= 80:
                st.success("**[Clean Operation]** 탄소 발생이 매우 적습니다.")
            elif cfe_score >= 40:
                st.warning("**[Transition State]** 한전 전력 의존도를 낮출 필요가 있습니다.")
            else:
                st.error("**[High Carbon Risk]** 무탄소 에너지원 확대를 검토하십시오.")

            st.info(f"""
            * **운영 데이터 분석**: 현재 소비 중인 {total_load:,}kW 중 {total_cfe_supply:,}kW({cfe_score:.1f}%)를 무탄소 전원으로 충당하고 있으며, 부족분 {net_grid_pwr:,}kW를 한전(그리드)으로부터 수전하고 있습니다.
            """)
            
            
        else:
            st.info("데이터를 입력하고 분석 버튼을 눌러주세요.")