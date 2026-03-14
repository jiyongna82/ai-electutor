import streamlit as st
import pandas as pd
from datetime import datetime

def run_calc():
    now = datetime.now()
    current_m = now.month

    st.subheader(f"🍃 6-3. 외기 냉방(Free Cooling) 경제성 시뮬레이션")
    st.caption("설비별 정격 전력과 실시간 사용률(%)을 반영하여 더욱 정밀한 연간 절감액을 산출합니다.")

    # [데이터베이스] 권역별 월평균 기온 (℃)
    regional_temp_db = {
        "서울/경기": [ -2.4, 0.5, 6.3, 12.9, 18.7, 23.1, 25.8, 26.3, 21.6, 15.0, 7.3, -0.1 ],
        "강원": [ -4.1, -0.8, 5.1, 12.1, 18.2, 22.7, 25.4, 25.6, 20.3, 13.0, 5.6, -1.5 ],
        "충청": [ -1.0, 1.8, 7.4, 13.8, 19.4, 23.6, 26.3, 26.7, 21.9, 15.1, 7.9, 0.9 ],
        "경상": [ 0.2, 2.7, 8.3, 14.7, 20.1, 24.1, 26.8, 27.3, 22.4, 15.9, 8.8, 1.9 ],
        "전라": [ 0.6, 2.3, 7.2, 13.2, 18.6, 22.8, 26.1, 26.5, 22.0, 15.6, 9.1, 2.8 ],
        "제주": [ 6.1, 6.8, 9.4, 14.1, 18.2, 21.6, 25.5, 27.1, 23.9, 19.1, 13.5, 8.3 ]
    }

    # [데이터베이스] 한전 요금제 (kWh당 평균 단가)
    tariff_db = {
        "산업용(갑) 고압": 128,
        "산업용(을) 고압A - 선택 II": 145,
        "산업용(을) 고압B - 선택 II": 155,
        "산업용(을) 고압C - 선택 III": 165
    }

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### 📥 1. 냉방 설비 그룹 설정 (사용률 반영)")
        num_groups = st.slider("설비 그룹 수", 1, 5, 1)
        
        total_effective_pwr = 0
        for i in range(num_groups):
            with st.expander(f"설비 그룹 #{i+1}", expanded=True):
                c1, c2 = st.columns(2)
                rated_pwr = c1.number_input(f"정격 소비전력 (kW) #{i+1}", value=400, step=10, key=f"rp_{i}")
                load_factor = c2.slider(f"평균 사용률 (%) #{i+1}", 0, 100, 75, key=f"lf_{i}")
                
                # 실질 소모 전력 계산
                effective_pwr = rated_pwr * (load_factor / 100)
                total_effective_pwr += effective_pwr
                st.caption(f"📍 그룹 #{i+1} 실질 소모 전력: **{effective_pwr:.1f} kW**")

        st.markdown("---")
        st.markdown("#### 🌍 2. 지역 및 요금제 설정")
        selected_region = st.selectbox("분석 대상 권역", list(regional_temp_db.keys()), index=0)
        selected_tariff = st.selectbox("한전 요금제 선택", list(tariff_db.keys()), index=1)
        elec_price = tariff_db[selected_tariff]
        
        free_limit_temp = st.slider("프리쿨링 전환 외기온도 (℃)", 5.0, 15.0, 7.0, 0.5)

        btn = st.button("사용률 기반 정밀 시뮬레이션 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {selected_region} 분석 리포트")
        if btn:
            temps = regional_temp_db[selected_region]
            free_months = [i+1 for i, t in enumerate(temps) if t <= free_limit_temp]
            num_free_months = len(free_months)
            
            # 실질 소모 전력 기반 절감량 산출
            monthly_save_kwh = total_effective_pwr * 24 * 30
            annual_save_kwh = monthly_save_kwh * num_free_months
            annual_save_money = annual_save_kwh * elec_price

            res_df = pd.DataFrame([
                {"분석 항목": "통합 유효 소비전력", "데이터": f"{total_effective_pwr:,.1f} kW", "상태": "⚙️ 사용률 반영"},
                {"분석 항목": "프리쿨링 가용 기간", "데이터": f"연간 {num_free_months}개월", "상태": f"📅 {free_months}월"},
                {"분석 항목": "연간 총 절감량", "데이터": f"{annual_save_kwh:,.0f} kWh", "상태": "🔋 전력절감"},
                {"분석 항목": "연간 예상 절감액", "데이터": f"{annual_save_money:,.0f} 원", "상태": "💰 OPEX 개선"}
            ])
            
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            st.metric(f"연간 예상 절감 비용", f"{annual_save_money:,.0f} 원")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운영 인사이트")
            st.info(f"""
            1. **사용률의 중요성:** 정격 전력 대비 평균 **사용률({total_effective_pwr/sum([400]*num_groups)*100:.1f}%)**을 적용하여 과다 산출을 방지했습니다. 이는 실제 PUE 개선분과 더 밀접하게 동기화됩니다.
            2. **냉방 부하 특성:** 외기 온도가 높은 하계에는 사용률이 상승하지만, 프리쿨링 시점(동계/환절기)에는 IT 부하 위주로 운전되므로 상대적으로 낮은 사용률이 적용되는 것이 현실적입니다.
            3. **투자 회수(ROI):** 연간 {annual_save_money:,.0f}원의 절감액은 고효율 열교환기나 자동 제어 시스템 도입 시 투자 회수 기간을 산정하는 기준 지표가 됩니다.
            """)
            
            
        else:
            st.info("정격 전력과 예상 사용률을 입력하여 실제에 가까운 절감액을 확인하십시오.")