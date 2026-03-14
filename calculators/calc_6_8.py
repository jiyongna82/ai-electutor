import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("❄️ 6-8. 냉동기 대수 제어 및 델타T(ΔT) 효율 분석")
    st.caption("실시간 냉동기 부하율과 냉수 온도차(ΔT)를 분석하여 최적의 대수 제어 시나리오를 제시합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 냉방 시스템 운전 현황")
        rated_capa = st.number_input("냉동기 대당 정격 용량 (USRT)", value=400, step=10)
        operating_count = st.number_input("현재 가동 대수 (대)", value=2, min_value=1)
        
        st.markdown("---")
        st.markdown("#### 🌡️ 2. 냉수 온도 계측")
        supply_temp = st.number_input("공급 냉수 온도 (Supply, ℃)", value=7.0, step=0.5)
        return_temp = st.number_input("환수 냉수 온도 (Return, ℃)", value=12.0, step=0.5)
        
        st.markdown("---")
        st.markdown("#### 💧 3. 유량 계측 데이터")
        total_flow = st.number_input("총 냉수 유량 (m³/h)", value=300.0, step=10.0)

        btn = st.button("냉방 효율 및 대수 최적화 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 냉동기 효율 및 대수 제어 분석")
        if btn:
            # --- 계산 로직 ---
            # 1. 델타T 산출
            delta_t = return_temp - supply_temp
            
            # 2. 현재 냉방 부하 산출 (kcal/h -> USRT 환산)
            # Q = m * C * delta_t (비열 C=1로 가정)
            cooling_load_kcal = total_flow * 1000 * delta_t
            current_usrt = cooling_load_kcal / 3024 # 1 USRT = 3,024 kcal/h
            
            # 3. 냉동기 부하율 및 최적 대수 산출
            total_rated_usrt = rated_capa * operating_count
            load_factor = (current_usrt / total_rated_usrt) * 100
            
            # 최적 대수 제안 (부하율 70~80% 기준)
            suggested_count = max(1, round(current_usrt / (rated_capa * 0.75)))

            # --- 결과 표시 ---
            if 60 <= load_factor <= 85:
                l_status, l_color = "✅ 적정 (Optimal)", "green"
            elif load_factor < 60:
                l_status, l_color = "⚠️ 저부하 (Low Load)", "orange"
            else:
                l_status, l_color = "🚨 과부하 (Overload)", "red"

            res_df = pd.DataFrame([
                {"분석 지표": "현재 총 냉방 부하", "데이터": f"{current_usrt:.1f} USRT", "판정": "📊 분석"},
                {"분석 지표": "냉수 온도차 (ΔT)", "데이터": f"{delta_t:.1f} ℃", "판정": "🌡️ 양호" if delta_t >= 5 else "⚠️ 낮음"},
                {"분석 지표": "냉동기 평균 부하율", "데이터": f"{load_factor:.1f} %", "판정": l_status},
                {"분석 지표": "권장 가동 대수", "데이터": f"{suggested_count} 대", "판정": "⚙️ 제안"}
            ])
            
            st.dataframe(
                res_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "분석 지표": st.column_config.TextColumn("분석 지표", width="medium"),
                    "데이터": st.column_config.TextColumn("데이터", width="small"),
                    "판정": st.column_config.TextColumn("판정", width="small")
                }
            )

            st.metric("현재 시스템 ΔT", f"{delta_t:.1f} ℃", delta=f"{delta_t - 5.0:.1f} ℃ (기준 5℃)")

            st.markdown("---")
            st.markdown("##### 💡 냉방 운영 전문가 가이드")
            
            if delta_t < 5.0:
                st.warning(f"**[Low Delta T Syndrome]** 온도차({delta_t}℃)가 너무 낮습니다. 유량이 과다하여 펌프 동력이 낭비되고 있습니다. 바이패스 밸브 개도 및 말단 차압을 재점검하십시오.")
            
            if suggested_count < operating_count:
                st.info(f"**[대수 제어 제안]** 현재 부하({current_usrt:.1f} USRT) 대비 가동 대수가 많습니다. 냉동기를 {suggested_count}대로 감축 운전하여 효율 구간(75~80%) 진입을 권고합니다.")

            st.info(f"""
            1. **ΔT의 중요성:** 데이터센터는 고현열 부하 특성을 가지므로, ΔT를 최대한 크게 유지하는 것이 시스템 전체의 COP를 높이는 지름길입니다.
            2. **펌프 동력 절감:** ΔT가 1℃ 상승할 때마다 동일 부하 대비 유량(LPM)을 줄일 수 있어 펌프 인버터 제어를 통한 큰 에너지 절감이 가능합니다.
            3. **운전 대수 최적화:** 냉동기는 부분 부하 효율보다 정격 부하의 70~80% 구간에서 가장 효율이 좋습니다.
            """)
            
            
        else:
            st.info("냉동기 운전 데이터와 온도 계측값을 입력하여 냉방 효율을 진단하십시오.")