import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-6. 순간 전압 강하(Voltage Sag) 및 장비 정지 위험 분석")
    st.caption("계통 사고 시 발생하는 전압 새그(Sag)의 깊이와 지속 시간을 바탕으로 ITIC(CBEMA) 커브 기준 장비의 안전성을 평가합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전압 새그(Sag) 측정 데이터")
        v_nominal = st.selectbox("정격 전압 (V)", [220, 380, 440, 6600, 22900], index=0)
        
        # 새그 발생 시 잔류 전압 (Magnitude)
        v_sag_pct = st.slider("새그 잔류 전압 (%)", 0, 100, 70, 5, help="정격 대비 남아있는 전압의 크기입니다. 낮을수록 위험합니다.")
        v_actual = v_nominal * (v_sag_pct / 100)
        
        # 새그 지속 시간 (Duration)
        duration_ms = st.number_input("지속 시간 (ms)", min_value=1, value=100, step=10)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 장비 민감도 판정 기준")
        std_type = st.radio("적용 표준", ["ITIC (CBEMA) 표준", "SEMI F47 표준"], horizontal=True)

        btn = st.button("새그 영향성 정밀 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 ITIC 커브 기반 안전성 진단")
        if btn:
            # ITIC (CBEMA) Ride-Through 판정 로직 (간략화된 공학 모델)
            is_safe = True
            diagnosis = ""
            
            if duration_ms <= 20: # 1.2 Cycles (60Hz 기준)
                if v_sag_pct < 0: # 무전압 허용 (대개 20ms까지는 커패시터로 버팀)
                    is_safe = True
                diagnosis = "초단시간 새그: 장비 내부 커패시터로 보상 가능한 영역입니다."
            elif duration_ms <= 500: # 0.5초 이내
                if v_sag_pct < 70: 
                    is_safe = False
                    diagnosis = "단시간 새그: 전압 저하가 심하여 IT 장비의 전원부(PSU)가 정지될 수 있습니다."
                else:
                    diagnosis = "안전 영역: 전압 저하가 있으나 장비가 가동을 유지할 수 있는 범위입니다."
            else: # 지속적 저전압 (Over 0.5s)
                if v_sag_pct < 80:
                    is_safe = False
                    diagnosis = "지속적 저전압: 장기적인 전압 강하로 인해 시스템 다운이 예상됩니다."
                else:
                    diagnosis = "정상 범위: 허용 한도 내의 전압 변동입니다."

            # --- 결과 시각화 ---
            if is_safe:
                st.success(f"✅ 진단 결과: **장비 운전 유지 가능 (Ride-Through)**")
                st.info(f"📝 분석: {diagnosis}")
            else:
                st.error(f"❌ 진단 결과: **장비 정지(Trip) 위험 구역**")
                st.warning(f"📝 분석: {diagnosis}")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("잔류 전압 (Magnitude)", f"{v_sag_pct} %", f"{v_actual:.1f} V")
            res_c2.metric("지속 시간 (Duration)", f"{duration_ms} ms", f"{(duration_ms/16.67):.1f} Cycles")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **Voltage Sag의 정의:** 계통의 낙뢰 사고나 대용량 부하의 기동 시, 전압이 0.5사이클에서 수 초 동안 정격의 **10~90%**로 떨어지는 현상입니다.
            2. **ITIC (CBEMA) 곡선의 중요성:** 서버나 정밀 제어기기는 전압이 일정 수준 이하로 떨어지면 데이터 손실 방지를 위해 스스로 셧다운됩니다. 이 곡선을 통해 **UPS(무정전전원장치)**의 필요성을 검토할 수 있습니다.
            3. **현장 조치 사항:** 만약 진단 결과가 **'위험'**으로 나온다면, 해당 분전반에 **STS(Static Transfer Switch)**를 설치하거나 장비 자체의 **Ride-Through 능력**이 보강된 제품을 선정해야 합니다.
            """)
            
            st.latex(r"Sag \ Magnitude [\%] = \frac{V_{rms}}{V_{nominal}} \times 100")
            
        else:
            st.info("새그 데이터(크기, 시간)를 입력하여 장비의 안정성을 시뮬레이션하십시오.")