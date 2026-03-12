import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🧪 6-10. 액침 냉각(Immersion Cooling) 효율 및 에너지 분석")
    st.caption("비전도성 액체에 서버를 직접 담가 냉각하는 액침 냉각 방식의 열전달 효율과 PUE 개선 효과를 분석합니다.")

    # --- 액침 냉각(Immersion Cooling) 개요 ---
    with st.expander("📘 액침 냉각 기술 가이드", expanded=False):
        st.markdown("""
        **액침 냉각(Immersion Cooling)**은 고밀도 AI 서버(GPU 등)의 발열을 해결하기 위한 차세대 냉각 기술입니다.
        
        * **직접 냉각**: 공기보다 열전도율이 1,000배 이상 높은 **유전체 용액(Dielectric Fluid)**에 서버를 직접 침전시킵니다.
        * **에너지 절감**: 서버 내부 팬(Fan) 제거가 가능하며, 공조기(CRAH/FWU) 동력을 90% 이상 절감하여 PUE 1.1 이하를 달성합니다.
        * **고밀도 구현**: 랙당 50kW~100kW 이상의 초고밀도 실장이 가능해집니다.
        """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 액침 탱크(Tank) 운전 데이터")
        server_it_load = st.number_input("IT 장비 부하 (kW)", value=50.0, step=5.0, help="탱크 1개당 서버 소비 전력 합계")
        
        st.markdown("---")
        st.markdown("#### 🌡️ 2. 유전체 용액(Fluid) 온도")
        fluid_in = st.number_input("용액 공급 온도 (Inlet, ℃)", value=35.0, step=0.5)
        fluid_out = st.number_input("용액 환수 온도 (Outlet, ℃)", value=45.0, step=0.5)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 3. 비교군 (기존 공냉식 설정)")
        fan_pwr_ratio = st.slider("기존 서버 팬(Fan) 전력 비중 (%)", 5, 20, 15, help="공냉식일 때 서버 내부 팬이 차지하던 전력 비중")
        air_pue = st.number_input("기존 공냉식 PUE", value=1.5, step=0.1)

        btn = st.button("액침 냉각 효율 시뮬레이션 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 PUE 개선 리포트")
        if btn:
            # --- 분석 로직 ---
            # 1. 냉각 효율(Delta T)
            delta_t = fluid_out - fluid_in
            
            # 2. 서버 팬 제거에 따른 실질 IT 부하 절감액
            saved_fan_pwr = server_it_load * (fan_pwr_ratio / 100)
            reduced_it_load = server_it_load - saved_fan_pwr
            
            # 3. 액침 냉각 PUE 추정 (공조 동력 급감 반영)
            # 통상 액침 냉각은 부속 펌프/CDU 동력만 추가되므로 1.03~1.05 수준
            immersion_pue = 1.05 
            
            # 4. 연간 에너지 절감량 (kWh/Year)
            annual_save_kwh = (server_it_load * air_pue - reduced_it_load * immersion_pue) * 24 * 365

            # 데이터프레임 구성
            res_data = {
                "분석 지표": ["용액 온도차 (ΔT)", "서버 팬 제거 이득", "예상 Immersion PUE", "연간 예상 전력 절감"],
                "데이터": [f"{delta_t:.1f} ℃", f"{saved_fan_pwr:.1f} kW", f"{immersion_pue}", f"{annual_save_kwh:,.0f} kWh"],
                "상태": ["✅ 우수", "📉 부하감소", "🏆 최적", "💰 비용절감"]
            }
            
            st.dataframe(
                pd.DataFrame(res_data),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "분석 지표": st.column_config.TextColumn("분석 지표", width="medium"),
                    "데이터": st.column_config.TextColumn("데이터", width="small"),
                    "상태": st.column_config.TextColumn("상태", width="small")
                }
            )

            st.metric("PUE 개선 폭", f"{air_pue} → {immersion_pue}", delta=f"-{(air_pue - immersion_pue):.2f}")

            st.markdown("---")
            st.markdown("##### 💡 운영 전문가 기술 제언")
            
            if delta_t < 5:
                st.warning("**[유량 과다]** 용액 온도차(ΔT)가 너무 낮습니다. CDU 펌프 속도를 조절하여 펌프 동력을 추가 절감하십시오.")
            
            st.info(f"""
            1. **에너지 시너지:** 액침 냉각은 서버 내부의 팬을 제거하므로 IT 부하 자체가 {saved_fan_pwr:.1f}kW만큼 줄어드는 **'역부하 효과'**가 발생합니다.
            2. **폐열 회수:** 환수 온도({fluid_out}℃)가 고온으로 유지되므로, 인근 사무동 난방이나 온수 공급 등 **폐열 재활용(Waste Heat Reuse)**에 매우 유리합니다.
            3. **유지보수:** 용액의 오염도와 산가(Acid Number)를 정기적으로 측정하여 절연 성능을 관리하는 것이 핵심입니다.
            """)
            
            
        else:
            st.info("액침 냉각 탱크의 온도와 부하 데이터를 입력하여 효율을 분석하십시오.")