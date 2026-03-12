import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("🔋 5-6. 에너지 저장 장치(ESS) 피크컷 및 범용 요금제 분석")
    st.caption("산업용 전 요금제(선택 I,II,III)를 반영하여 ESS의 피크컷 및 부하이전 경제성을 정밀 분석합니다.")

    # [범용 요금제 데이터베이스] 선택 I, II, III 전체 라인업 반영
    tariff_db = {
        "고압 A - 선택 I": {"base": 7580, "cheap": 85.2, "peak": 198.5},
        "고압 A - 선택 II": {"base": 8320, "cheap": 78.5, "peak": 218.4},
        "고압 A - 선택 III": {"base": 9540, "cheap": 72.1, "peak": 232.0},
        "고압 B - 선택 I": {"base": 7920, "cheap": 82.4, "peak": 208.5},
        "고압 B - 선택 II": {"base": 8850, "cheap": 75.2, "peak": 228.6},
        "고압 B - 선택 III": {"base": 10210, "cheap": 68.4, "peak": 241.0},
        "고압 C - 선택 II": {"base": 9230, "cheap": 72.8, "peak": 238.2},
        "고압 C - 선택 III": {"base": 10580, "cheap": 66.5, "peak": 249.5}
    }

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. ESS 및 수전 환경")
        ess_capa = st.number_input("ESS 배터리 용량 (kWh)", value=1000, step=100)
        dod = st.slider("방전 심도 (DOD, %)", 50, 100, 90)
        
        # 전체 선택 요금제 리스트
        selected_type = st.selectbox("적용 전력 요금제 선택", list(tariff_db.keys()), index=4)
        current_season = st.radio("운용 계절", ["하계", "동계", "춘추계"], horizontal=True)
        
        st.markdown("---")
        st.markdown("#### ⚡ 2. 운용 파라미터")
        season_mult = 1.15 if current_season in ["하계", "동계"] else 0.95
        
        base_rate = tariff_db[selected_type]["base"]
        c_price = tariff_db[selected_type]["cheap"]
        d_price = st.number_input("최대부하 방전 단가 (원/kWh)", value=float(tariff_db[selected_type]["peak"] * season_mult))
        
        peak_cut_target = st.number_input("목표 피크 저감량 (kW)", value=200, step=10)
        round_eff = st.slider("충방전 효율 (%)", 70, 98, 90)

        btn = st.button("경제성 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {selected_type} 분석 리포트")
        if btn:
            # --- 경제성 계산 ---
            usable_kwh = ess_capa * (dod / 100)
            charge_needed = usable_kwh / (round_eff / 100)
            
            daily_save = (usable_kwh * d_price) - (charge_needed * c_price)
            monthly_usage_save = daily_save * 30
            monthly_base_save = peak_cut_target * base_rate
            total_save = monthly_usage_save + monthly_base_save
            
            # --- 결과 데이터프레임 (인덱스 제거 적용) ---
            res_df = pd.DataFrame([
                {"항목": "수전 요금제", "데이터": selected_type},
                {"항목": "기본료 단가", "데이터": f"{base_rate:,} 원/kW"},
                {"항목": "경부하 충전가", "데이터": f"{c_price:.1f} 원/kWh"},
                {"항목": "최대부하 방전가", "데이터": f"{d_price:.1f} 원/kWh"},
                {"항목": "월간 기본료 절감", "데이터": f"{monthly_base_save:,.0f} 원"},
                {"항목": "월간 사용량 절감", "데이터": f"{monthly_usage_save:,.0f} 원"}
            ])
            
            # hide_index=True를 통해 좌측 숫자(0,1,2,3...) 삭제
            st.dataframe(res_df, hide_index=True, use_container_width=True)

            st.metric("예상 월 총 절감액", f"{total_save:,.0f} 원")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운영 제언")
            st.info(f"""
            1. **요금제 전략:** 현재 선택하신 **{selected_type}**은 부하율이 높은 대규모 센터에 적합하며, 기본요금 비중이 커 피크컷 효율이 매우 높습니다.
            2. **효율의 가치:** 충방전 효율 {round_eff}%에서 발생하는 손실을 줄이기 위해 배터리 온도 관리(Cooling) 최적화가 필수적입니다.
            3. **피크 관리:** {peak_cut_target}kW의 피크 저감 실현을 위해 한전 검침 주기와 연동된 실시간 전력 제어(EMS)가 수반되어야 합니다.
            """)
            
            
        else:
            st.info("요금제와 ESS 사양을 입력하여 인덱스 없이 깔끔한 분석 결과를 확인하십시오.")