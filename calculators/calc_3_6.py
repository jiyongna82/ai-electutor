import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-6. 펌프 및 송풍기(Fan) 설계 동력 및 에너지 절감 분석")
    st.caption("유체의 유량, 양정(압력) 데이터를 바탕으로 필요 동력을 산출하고, VFD 적용 시의 에너지 절감률을 시뮬레이션합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 유체기계 사양 입력")
        
        load_type = st.radio("부하 종류", ["원심 펌프 (Pump)", "송풍기 (Fan/Blower)"], horizontal=True)
        
        if load_type == "원심 펌프 (Pump)":
            flow = st.number_input("유량 (m³/min)", min_value=0.1, value=2.0, step=0.1)
            head = st.number_input("전양정 (m)", min_value=1.0, value=30.0, step=1.0)
            gravity = 9.8  # 비중량 관련 상수
        else:
            flow = st.number_input("풍량 (m³/min)", min_value=0.1, value=100.0, step=10.0)
            head = st.number_input("정압 (mmAq)", min_value=1.0, value=50.0, step=5.0)
            gravity = 1/102 # 풍량 단위 환산 상수

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 효율 및 VFD 제어 조건")
        eff = st.slider("기계 효율 (%)", 40, 95, 75) / 100.0
        safety_factor = st.slider("설계 여유율 (K)", 1.0, 1.3, 1.1, 0.05)
        
        st.write("📊 **VFD 에너지 절감 시뮬레이션**")
        speed_ratio = st.slider("운전 회전수 비율 (%)", 50, 100, 80, 5) / 100.0

        btn = st.button("동력 분석 및 절감률 계산 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 시뮬레이션 결과")
        if btn:
            # 1. 수동력 및 축동력 계산
            if load_type == "원심 펌프 (Pump)":
                # P [kW] = (0.163 * Q * H * K) / eff (비중 1.0 가정)
                p_shaft = (0.163 * flow * head * safety_factor) / eff
            else:
                # P [kW] = (Q * H * K) / (6120 * eff)
                p_shaft = (flow * head * safety_factor) / (6120 * eff)
            
            # 2. 상사 법칙에 의한 절감 동력 계산 (P2 = P1 * (N2/N1)^3)
            p_vfd = p_shaft * (speed_ratio ** 3)
            saving_rate = (1 - (speed_ratio ** 3)) * 100

            # --- 결과 시각화 ---
            st.success(f"✅ 설계 축동력: **{p_shaft:.2f} kW**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric(f"VFD 운전 ({speed_ratio*100:.0f}%)", f"{p_vfd:.2f} kW")
            res_c2.metric("에너지 절감률", f"{saving_rate:.1f} %", delta=f"-{saving_rate:.1f}%")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **상사 법칙(Affinity Laws):** 유체기계의 유량은 회전수에 비례하고, 압력은 회전수의 제곱, **소비 전력은 회전수의 세제곱**에 비례합니다. 회전수를 20%만 줄여도 이론적으로 에너지를 약 **48.8%** 절감할 수 있습니다.
            2. **설계 여유율(K):** 펌프의 경우 통상 1.1, 송풍기의 경우 부하 변동을 고려하여 1.15~1.2 정도의 여유율을 적용하여 전동기 정격을 결정합니다.
            3. **VFD 적용 시 주의점:** 저속 운전 시 전동기 냉각 성능 저하와 배관 내 최소 유속(침전 방지 등)을 확인해야 합니다. 또한 정압이 높은 계통에서는 회전수를 너무 낮추면 유체가 흐르지 않는 **체절 운전** 상태가 될 수 있으므로 주의하십시오.
            """)
            
            st.latex(r"P_{shaft} = \frac{0.163 \cdot Q \cdot H \cdot K}{\eta} \quad [Pump]")
            st.latex(r"P_{vfd} = P_{shaft} \times \left( \frac{N_2}{N_1} \right)^3")
            
            
        else:
            st.info("좌측에 유체기계 사양을 입력하여 설계 동력과 절감률을 확인하십시오.")