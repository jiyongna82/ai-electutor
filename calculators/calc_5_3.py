import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("⛽ 5-3. 연료 공급 시스템 및 최장 운전 시간 분석")
    st.caption("유류 탱크 잔량과 발전기 부하율을 바탕으로 정전 시 데이터센터가 자립할 수 있는 최대 시간을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 🛢️ 1. 유류 저장 시설 현황")
        indoor_tank = st.number_input("실내 데이탱크(Day Tank) 합계 용량 (L)", value=16000, step=1000)
        outdoor_tank = st.number_input("옥외/지하 메인 탱크 합계 용량 (L)", value=114000, step=1000)
        current_fill_rate = st.slider("현재 유류 충진율 (%)", 0, 100, 80)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 발전기 운전 조건")
        num_gens = st.number_input("가동 발전기 수 (대)", min_value=1, value=5)
        gen_rated_kw = st.number_input("발전기 개별 정격 출력 (kW)", value=2500)
        load_factor = st.slider("실제 운전 부하율 (%)", 10, 100, 75)

        btn = st.button("운전 지속 시간 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 비상 전원 지속 시간 진단")
        if btn:
            # --- 계산 로직 ---
            # 1. 가용 연료량 (L)
            total_capacity = indoor_tank + outdoor_tank
            available_fuel = total_capacity * (current_fill_rate / 100)
            
            # 2. 연료 소비율 (BSFC 적용 모델링)
            # 일반적인 디젤 발전기는 1kWh당 약 0.24 ~ 0.26L를 소모함 (표준 0.25 적용)
            hourly_consumption_per_gen = gen_rated_kw * (load_factor / 100) * 0.25
            total_hourly_consumption = hourly_consumption_per_gen * num_gens
            
            # 3. 지속 시간 (Hours)
            endurance_hours = available_fuel / total_hourly_consumption if total_hourly_consumption > 0 else 0
            
            # --- 결과 테이블 구성 ---
            items = [
                {"항목": "총 유류 저장 용량", "수치": f"{total_capacity:,} L", "기준": "설계 용량", "판단": "✅ 확인"},
                {"항목": "현재 가용 연료량", "수치": f"{available_fuel:,} L", "기준": f"{current_fill_rate}% 충진", "판단": "✅ 양호" if current_fill_rate >= 80 else "⚠️ 충전권장"},
                {"항목": "시간당 총 소모량", "수치": f"{total_hourly_consumption:.1f} L/h", "기준": f"부하율 {load_factor}%", "판단": "📊 분석"},
                {"항목": "최장 가동 가능 시간", "수치": f"{endurance_hours:.1f} 시간", "기준": "연속 가동", "판단": "⏳ 계산"}
            ]
            
            res_df = pd.DataFrame(items)
            st.dataframe(res_df, hide_index=True, use_container_width=True)

            # --- 종합 결과 표시 ---
            st.metric("예상 전력 자립 시간", f"{endurance_hours:.1f} Hours", 
                      delta=f"{endurance_hours/24:.1f} Days", delta_color="normal")
            
            if endurance_hours >= 72:
                st.success(f"**[종합 판정]** 전력 자립 능력이 매우 우수합니다. (Tier-III 기준 72시간 충족)")
            elif endurance_hours >= 24:
                st.warning(f"**[종합 판정]** 24시간 이상 가동 가능하나, 장기 정전 시 외부 유류 보급 체계를 점검하십시오.")
            else:
                st.error(f"**[종합 판정]** 가용 시간이 부족합니다. 즉각적인 유류 보충 또는 비상 시 부하 제한(Load Shedding)이 필요합니다.")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운용 가이드")
            st.info(f"""
            1. **유류 이송 자동화:** 옥외 메인 탱크에서 실내 데이탱크로의 유류 이송 펌프(Transfer Pump) 연동 상태를 상시 확인하십시오.
            2. **연료 품질 관리:** 장기 저장 시 결로에 의한 수분 혼입이나 미생물 번식이 발생할 수 있으므로 정기적인 수분 드레인과 첨가제 관리가 중요합니다.
            3. **설계 팁:** 데이터센터 신뢰성을 위해 보통 **Full Load 기준 12~24시간**, **실부하 기준 48~72시간** 분량의 유류를 확보하는 것이 업계 표준입니다.
            """)
            
            
        else:
            st.info("저장 용량과 운전 조건을 입력하여 시스템의 생존 시간을 시뮬레이션하십시오.")