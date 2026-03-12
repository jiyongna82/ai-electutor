import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("⚡ 4-11. CTTS(무정전 절체) 동기 조건 및 안정성 분석")
    st.caption("한전과 비상발전기 간의 전압, 주파수, 위상을 비교하여 안전한 무정전 절체 가능 여부를 진단합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전원 전압 설정 (상간 전압)")
        # 6600V 기본값 유지
        u_volt = st.slider("한전 전압 (Utility, V)", min_value=380, max_value=7200, value=6600, step=1)
        g_volt = st.slider("발전기 전압 (Generator, V)", min_value=380, max_value=7200, value=6600, step=1)

        st.markdown("---")
        st.markdown("#### 📥 2. 주파수 및 위상차 설정")
        # 60.00Hz 및 0도 기본값 유지
        u_freq = st.slider("한전 주파수 (Hz)", min_value=59.0, max_value=61.0, value=60.0, step=0.01)
        g_freq = st.slider("발전기 주파수 (Hz)", min_value=59.0, max_value=61.0, value=60.0, step=0.01)
        phase_diff = st.slider("위상차 (Phase Angle, deg)", 0, 30, 0)

        st.markdown("---")
        st.markdown("#### ⚙️ 3. 동기 허용 오차 (IEEE 1547 기준)")
        v_limit = st.slider("전압차 허용 범위 (%)", 1.0, 10.0, 5.0, 0.5)
        f_limit = st.slider("주파수차 허용 범위 (Hz)", 0.05, 1.0, 0.2, 0.05)
        # 위상차 허용 범위를 5도로 고정/기본값 설정
        p_limit = st.slider("위상차 허용 범위 (deg)", 1, 20, 5)

        btn = st.button("동기화 정밀 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 실시간 동기 분석 리포트")
        if btn:
            # 1. 정밀 편차 계산
            dv_pct = abs(u_volt - g_volt) / u_volt * 100 if u_volt != 0 else 0
            df = abs(u_freq - g_freq)
            dp = abs(phase_diff)

            # 2. 판정 로직
            v_ok = dv_pct <= v_limit
            f_ok = df <= f_limit
            p_ok = dp <= p_limit
            can_transfer = v_ok and f_ok and p_ok

            # --- 결과 데이터프레임 구성 ---
            diag_data = [
                {"항목": "전압 편차", "측정치": f"{dv_pct:.2f} %", "기준": f"±{v_limit}%", "결과": "✅" if v_ok else "❌"},
                {"항목": "주파수 편차", "측정치": f"{df:.2f} Hz", "기준": f"±{f_limit}Hz", "결과": "✅" if f_ok else "❌"},
                {"항목": "위상차", "측정치": f"{dp} deg", "기준": f"±{p_limit}°", "결과": "✅" if p_ok else "❌"}
            ]
            st.dataframe(pd.DataFrame(diag_data), hide_index=True, use_container_width=True)

            if can_transfer:
                st.success(f"✅ **절체 가능:** {u_volt}V / {u_freq}Hz / {dp}° 조건이 동기 범위 내에 있습니다.")
            else:
                st.error("🚨 **절체 불가:** 설정된 동기 허용 범위를 벗어났습니다.")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드 (위상 동기)")
            st.info(f"""
            1. **엄격한 위상 관리:** 위상차 허용 범위를 **{p_limit}도**로 설정함으로써 투입 시 발생하는 서지 전류를 억제하고 발전기 가버너(Governor)에 가해지는 스트레스를 최소화합니다.
            2. **벡터도 해석:** 한전 전압 벡터와 발전기 전압 벡터가 거의 일치하는 시점에서 CTTS가 동작해야 합니다.
            3. **운전 권고:** 위상차가 지속적으로 발생할 경우 발전기의 동기 속도 제어 시스템을 점검하십시오.
            """)
            
            
            st.latex(r"\text{Phase Condition: } |\theta_u - \theta_g| \leq 5^\circ")
        else:
            st.info("슬라이더를 조절하여 동기 조건을 확인하십시오. (위상차 기준: 5도)")