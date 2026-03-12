import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("⚡ 6-4. STS(Static Transfer Switch) 고속 절체 및 신뢰성 분석")
    st.caption("반도체 소자(SCR) 기반의 고속 절체 시퀀스를 시뮬레이션하여 부하 가동 중단 위험을 진단합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 시스템 및 계통 상태")
        system_volt = st.selectbox("정격 전압 (V)", [208, 380, 440, 480], index=1)
        freq = st.radio("계통 주파수 (Hz)", [50, 60], index=1)
        
        st.markdown("---")
        st.markdown("#### ⏱️ 2. 절체 성능 파라미터")
        # STS 절체 시간 (통상 4ms 내외)
        transfer_time = st.number_input("절체 소요 시간 (ms)", value=4.0, step=0.5, 
                                        help="SCR 소자의 턴온/오프를 포함한 총 절체 시간입니다.")
        
        # 동기 상태 (위상차)
        phase_diff = st.slider("양원간 위상차 (Degree)", 0, 180, 5, 
                               help="위상차가 크면 절체 시 과도 전류(Inrush)가 발생할 수 있습니다.")

        st.markdown("---")
        st.markdown("#### 📉 3. 부하 허용 한계 (ITIC 기준)")
        # ITIC 커브의 무정전 허용 시간 기준 (일반적으로 20ms)
        itic_limit = st.slider("부하 무전원 허용 한계 (ms)", 10, 50, 20)

        btn = st.button("절체 신뢰성 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 STS 동작 건전성 진단 리포트")
        if btn:
            # --- 분석 로직 ---
            # 1. 절체 성공 여부 (ITIC 커브 기준)
            if transfer_time <= itic_limit:
                t_status, t_color = "✅ 성공 (Success)", "green"
            else:
                t_status, t_color = "🚨 실패 (Load Drop)", "red"
                
            # 2. 위상차에 따른 돌입 전류 위험도
            if phase_diff <= 10:
                p_risk = "안전 (Low Inrush)"
            elif phase_diff <= 30:
                p_risk = "주의 (Moderate Inrush)"
            else:
                p_risk = "위험 (High Inrush Risk)"

            # --- 결과 데이터프레임 (인덱스 제거) ---
            diag_df = pd.DataFrame([
                {"진단 항목": "절체 가용성", "데이터": f"{transfer_time} ms", "판정": t_status},
                {"항목": "ITIC 허용 마진", "데이터": f"{itic_limit - transfer_time:.1f} ms 여유", "판정": "📊 분석"},
                {"항목": "위상 동기 상태", "데이터": f"{phase_diff} °", "판정": p_risk},
                {"항목": "시스템 주파수", "데이터": f"{freq} Hz", "판정": "정상"}
            ])
            
            st.dataframe(diag_df, hide_index=True, use_container_width=True)

            # 핵심 메트릭
            st.metric("절체 속도 효율", f"{100 - (transfer_time/itic_limit*100):.1f} %", 
                      delta=f"Margin {itic_limit - transfer_time:.1f}ms")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 제언")
            
            if transfer_time > 8:
                st.warning(f"**[주의]** 절체 시간 {transfer_time}ms는 반사이클(8.33ms)에 근접합니다. SCR 소자의 노화나 제어 로직 점검이 필요합니다.")
            
            if phase_diff > 15:
                st.error(f"**[위험]** 양원간 위상차가 {phase_diff}°로 큽니다. 절체 시 변압기 포화나 차단기 오동작 가능성이 있으므로 동기화 장치(Sync-Check)를 점검하십시오.")

            st.info(f"""
            1. **ITIC(CBEMA) 커브 연동:** 대부분의 서버 파워(PSU)는 20ms 이하의 전압 강하를 견디도록 설계됩니다. 현재 {transfer_time}ms의 속도는 매우 안정적인 수준입니다.
            2. **무정전 절체 원리:** STS는 기계적 접점이 아닌 반도체 스위칭을 통해 Zero-crossing 지점에서 고속 절체를 수행하여 아크 발생을 억제합니다.
            3. **운영 팁:** 이중화된 UPS 계통의 위상차를 항상 10° 이내로 유지해야만 STS 절체 시 부하에 충격을 주지 않습니다.
            """)
            
            
            st.latex(r"I_{peak} \approx \frac{\sqrt{2} \cdot V_{L-L} \cdot \sin(\Delta\theta/2)}{X_{source}}")
        else:
            st.info("STS 제원과 계통 상태를 입력하여 절체 성공 가능성을 시뮬레이션하십시오.")