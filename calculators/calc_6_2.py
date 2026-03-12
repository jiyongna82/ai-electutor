import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🌬️ 6-2. 서버실 기류 차폐(Containment) 및 차압 분석")
    st.caption("컨테인먼트 내부와 외부의 차압, 온도를 분석하여 기류 우회(Bypass) 및 재순환(Recirculation) 위험을 진단합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 차폐 구역(Containment) 계측")
        containment_type = st.radio("차폐 방식 선택", ["Cold Aisle Containment (CAC)", "Hot Aisle Containment (HAC)"])
        
        # 실시간 계측값 입력
        st.markdown("---")
        inner_temp = st.number_input("차폐 구역 내부 온도 (℃)", value=22.0, step=0.5)
        outer_temp = st.number_input("차폐 구역 외부 온도 (℃)", value=28.0, step=0.5)
        
        # 차압 계측 (Pa)
        pressure_diff = st.number_input("내/외부 차압 (Static Pressure, Pa)", value=15.0, step=1.0, 
                                        help="권장 차압 범위: 10~25 Pa (IT 장비 팬 부하 고려)")
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 서버 랙(Rack) 현황")
        rack_count = st.slider("분석 구역 내 랙 수량", 1, 50, 20)
        blanking_panel_status = st.select_slider("블랭킹 패널 설치율", options=["0%", "25%", "50%", "75%", "100%"], value="100%")

        btn = st.button("기류 건전성 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 기류 분석 및 리포트")
        if btn:
            # --- 분석 로직 ---
            # 1. 차압 적정성 판정
            if 10 <= pressure_diff <= 25:
                p_status, p_color = "✅ 적정 (Optimal)", "green"
            elif pressure_diff > 25:
                p_status, p_color = "⚠️ 과다 (Over-pressure)", "orange"
            else:
                p_status, p_color = "🚨 부족 (Low-pressure)", "red"
                
            # 2. 온도차(Delta T) 분석
            delta_t = abs(outer_temp - inner_temp)
            if delta_t >= 8:
                t_status = "우수 (Good Separation)"
            else:
                t_status = "미흡 (Mixing Risk)"

            # --- 결과 데이터프레임 (인덱스 제거) ---
            diag_df = pd.DataFrame([
                {"진단 항목": "내/외부 차압 상태", "데이터": f"{pressure_diff} Pa", "상태": p_status},
                {"항목": "내/외부 온도 편차", "데이터": f"ΔT {delta_t:.1f} ℃", "상태": t_status},
                {"항목": "차폐 방식", "데이터": containment_type, "상태": "운용중"},
                {"항목": "기류 관리 수준", "데이터": blanking_panel_status, "상태": "양호" if blanking_panel_status == "100%" else "보완필요"}
            ])
            
            st.dataframe(diag_df, hide_index=True, use_container_width=True)

            # 핵심 지표 메트릭
            st.metric("현재 차압 (Static Pressure)", f"{pressure_diff} Pa", delta=f"{pressure_diff - 15.0:.1f} Pa")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기류 제언")
            
            if pressure_diff < 10:
                st.error("**[긴급]** 차압이 너무 낮습니다. 냉방기(FWU/CRAC) 풍량을 증대하거나 컨테인먼트 도어 밀폐 상태를 점검하십시오.")
            elif pressure_diff > 25:
                st.warning("**[주의]** 과도한 차압은 IT 장비 팬에 부하를 주어 고장의 원인이 될 수 있습니다. 송풍 속도 최적화가 필요합니다.")
            
            st.info(f"""
            1. **차압의 중요성:** {pressure_diff} Pa의 차압은 외부의 뜨거운 공기가 서버 입구로 유입되는 것을 방지하는 보이지 않는 벽입니다.
            2. **기류 혼합 방지:** 현재 온도차 {delta_t:.1f}℃는 기류 분리 효율을 나타냅니다. {blanking_panel_status}의 블랭킹 패널 설치는 랙 내부의 열 순환을 차단하는 필수 조치입니다.
            3. **효율 최적화:** 차압이 안정화되면 냉동기 공급 온도를 단계적으로 상향하여(최대 25~27℃) 추가적인 PUE 개선을 도모할 수 있습니다.
            """)
            
            
        else:
            st.info("실시간 차압 및 온도 데이터를 입력하여 서버실 기류 건전성을 진단하십시오.")