import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-10. 전동기 발열량 및 필요 냉각 공기량 분석")
    st.caption("전동기 운전 중 발생하는 손실 열량을 계산하고, 실내 온도를 목표치 이내로 유지하기 위한 필요 환기량을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 운전 조건")
        motor_kw = st.number_input("전동기 정격 출력 (kW)", min_value=0.1, value=75.0, step=5.0)
        eff = st.slider("전동기 운전 효율 (%)", 70.0, 98.0, 92.0) / 100.0
        load_factor = st.slider("운전 부하율 (%)", 10, 100, 80) / 100.0
        
        st.markdown("---")
        st.markdown("#### 🌡️ 2. 온도 및 환경 설정")
        # 현재 온도와 목표 온도를 분리하여 입력
        t_in = st.number_input("현재 흡입 공기 온도 (℃)", min_value=-10.0, max_value=50.0, value=25.0, step=1.0)
        t_limit = st.number_input("실내 목표 제한 온도 (℃)", min_value=0.0, max_value=60.0, value=35.0, step=1.0)
        
        # 허용 온도 차 (Design Temperature Rise) 자동 계산
        delta_t = t_limit - t_in
        
        if delta_t <= 0:
            st.error("⚠️ 목표 온도는 현재 온도보다 높아야 합니다.")
            delta_t = 1  # 계산 오류 방지용 최소값
        else:
            st.info(f"💡 **설계 온도 상승 한도(ΔT): {delta_t:.1f} ℃**")
        
        btn = st.button("냉각 필요량 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 진단 결과")
        if btn:
            # 1. 전동기 손실 발열량(Q) 산출
            # Q = P_out * (1/η - 1) * 부하율
            p_loss_kw = (motor_kw * load_factor) * ((1 / eff) - 1)
            q_kcal_h = p_loss_kw * 860  # 1kW = 860 kcal/h
            
            # 2. 필요 냉각 공기량(V) 산출
            # V [m³/h] = Q [kcal/h] / (Cp * ρ * ΔT)
            # 공기 정압비열 0.24 kcal/kg·℃, 밀도 1.2 kg/m³ 적용
            v_m3_h = q_kcal_h / (0.24 * 1.2 * delta_t)
            v_m3_min = v_m3_h / 60

            # --- 결과 시각화 ---
            st.success(f"✅ 발생 손실 전력: **{p_loss_kw:.2f} kW**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("총 발열량", f"{int(q_kcal_h)} kcal/h")
            res_c2.metric("필요 환기량", f"{v_m3_min:.1f} CMM")
            
            st.write(f"- 시간당 필요 풍량: **{v_m3_h:.1f} CMH**")
            st.write(f"- 현재 대비 온도 상승 한계: **{delta_t} ℃**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **설계 온도 상승 한도(ΔT):** 실내의 쾌적함과 장비 수명을 위해 통상적으로 **5~10℃** 내외로 설정합니다. 이 값이 작을수록 더 많은 환기량이 필요합니다.
            2. **열평형 유지:** 전동기에서 발생하는 열량(**{int(q_kcal_h)} kcal/h**)을 환기 시스템이 외부로 배출하지 못하면 실내 온도는 목표치인 **{t_limit}℃**를 초과하게 됩니다.
            3. **현장 조치:** 필요 환기량이 확보되지 않을 경우, 강제 배기 팬을 추가하거나 외기 유입 온도를 낮추는 프리쿨링(Pre-cooling) 기법을 검토해야 합니다.
            """)
            
            st.latex(r"Q_{loss} = P_{out} \times \left( \frac{1}{\eta} - 1 \right) \times Load \ Factor")
            st.latex(r"V [m^3/h] = \frac{Q [kcal/h]}{0.288 \times (T_{limit} - T_{in})}")
            
            
        else:
            st.info("입구 온도와 목표 온도를 입력하여 냉각 시스템을 시뮬레이션하십시오.")