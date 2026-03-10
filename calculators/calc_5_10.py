import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🌱 5-10. 탄소배출권 및 RE100 이행 지표 산출")
    st.caption("지역별 일조 데이터와 실시간 부하를 연동하여 월간 탄소 배출량 및 RE100 달성률을 정밀 분석합니다.")

    # [지역별 연평균 일조시간 데이터베이스] - 국내 주요 지역 통계 반영
    sun_hours_db = {
        "서울/경기": 3.4,
        "강원": 3.7,
        "충청": 3.6,
        "전라": 3.8,
        "경상": 3.9,
        "제주": 3.5
    }

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 실시간 에너지 소비 데이터")
        current_pwr_kw = st.number_input("현재 실시간 전력 부하 (kW)", value=1500, step=100)
        # 월간 총 사용량 환산 (kW * 24h * 30d / 1000)
        monthly_est_mwh = (current_pwr_kw * 24 * 30) / 1000
        
        st.markdown("---")
        st.markdown("#### ♻️ 2. 신재생 에너지 조달 (체크 시 반영)")
        
        # [태양광 발전 상세 설정]
        use_pv = st.checkbox("자가발전(PV) 사용", value=True)
        if use_pv:
            selected_region = st.selectbox("발전 지역 선택", list(sun_hours_db.keys()), index=4)
            daily_sun_hour = sun_hours_db[selected_region]
            
            # 현재 시각 발전량을 입력받아 설비 용량 대비 발전 효율을 추정하거나, 
            # 일일 평균 발전량으로 환산 (현재 발전량 기반 시뮬레이션)
            pv_now_kw = st.number_input("현재 태양광 발전 출력 (kW)", value=300, step=10)
            st.caption(f"📍 {selected_region} 지역 평균 일조시간: {daily_sun_hour}시간/일")
            
            # 월간 PV 발전량 환산 (현재 출력 기반 일조시간 적용)
            # (현재 출력 기준이 일일 피크 부근이라 가정할 때의 월간 기대값)
            pv_monthly_mwh = (pv_now_kw * daily_sun_hour * 30) / 1000
        else:
            pv_monthly_mwh = 0.0
        
        # [기타 조달 방식]
        use_rec = st.checkbox("REC 구매분 반영", value=True)
        rec_val = st.number_input("월간 REC 구매량 (MWh)", value=150.0, step=10.0) if use_rec else 0.0
        
        use_ppa = st.checkbox("PPA/녹색프리미엄 반영", value=False)
        ppa_val = st.number_input("월간 PPA 계약량 (MWh)", value=100.0, step=10.0) if use_ppa else 0.0
        
        st.markdown("---")
        st.markdown("#### 💰 3. 환경 파라미터")
        emission_factor = st.number_input("배출계수 (tCO2eq/MWh)", value=0.4594, format="%.4f")
        kau_price = st.number_input("탄소배출권 단가 (원/tCO2eq)", value=15000, step=500)

        btn = st.button("ESG 경영 지표 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 RE100 및 탄소중립 시뮬레이션")
        if btn:
            # --- 계산 로직 ---
            total_re_mwh = pv_monthly_mwh + rec_val + ppa_val
            re100_rate = (total_re_mwh / monthly_est_mwh * 100) if monthly_est_mwh > 0 else 0
            
            # 탄소 배출량 (신재생 사용분 제외 후 계산)
            net_mwh = max(0, monthly_est_mwh - total_re_mwh)
            carbon_emissions = net_mwh * emission_factor
            
            # 절감 가치 계산
            potential_emissions = monthly_est_mwh * emission_factor
            saved_carbon = potential_emissions - carbon_emissions
            saving_value = saved_carbon * kau_price

            # --- 결과 데이터프레임 (인덱스 제거) ---
            res_df = pd.DataFrame([
                {"분석 지표": "월간 예상 소비량", "데이터": f"{monthly_est_mwh:,.1f} MWh"},
                {"분석 지표": "월간 PV 기대 발전량", "데이터": f"{pv_monthly_mwh:,.1f} MWh"},
                {"분석 지표": "RE100 이행 총량", "데이터": f"{total_re_mwh:,.1f} MWh"},
                {"분석 지표": "RE100 달성률", "데이터": f"{re100_rate:.2f} %"},
                {"분석 지표": "예상 탄소 배출량", "데이터": f"{carbon_emissions:,.2f} tCO2eq"},
                {"분석 지표": "배출권 비용 절감", "데이터": f"{saving_value:,.0f} 원"}
            ])
            
            st.dataframe(res_df, hide_index=True, use_container_width=True)

            st.metric("최종 탄소 중립 지수", f"{re100_rate:.1f} %", delta=f"{saved_carbon:,.1f} tCO2 절감")

            st.markdown("---")
            st.markdown("##### 💡 전문가 ESG 코멘트")
            if re100_rate >= 100:
                st.success("**[Net Zero 달성]** 센터 소비량 전량을 신재생 에너지로 상쇄하고 있습니다.")
            else:
                st.warning(f"**[추가 조달 필요]** 현재 달성률은 {re100_rate:.1f}%입니다. 목표치 달성을 위해 약 {max(0, monthly_est_mwh - total_re_mwh):,.1f} MWh의 추가 조달이 필요합니다.")

            st.info(f"""
            1. **태양광 분석:** {selected_region} 지역의 평균 일조시간(**{daily_sun_hour}h**)을 적용하여 현재 출력 **{pv_now_kw}kW** 기준 월간 발전량을 산출했습니다.
            2. **경제적 가치:** 탄소배출권 가격 {kau_price:,}원을 기준으로 신재생 에너지 활용을 통해 월간 **{saving_value:,.0f}원**의 환경 비용을 절감했습니다.
            3. **조달 전략:** 자가발전 비중이 낮을 경우, REC 구매나 PPA 계약을 통해 RE100 이행률을 탄력적으로 조정할 수 있습니다.
            """)
            
            
        else:
            st.info("데이터를 입력하여 지역별 특성이 반영된 RE100 지표를 시뮬레이션하십시오.")