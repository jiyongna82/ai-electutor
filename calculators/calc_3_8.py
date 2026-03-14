import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-8. 승강기(엘리베이터)용 전동기 소요 동력 산출")
    st.caption("적재 하중, 운행 속도 및 균형추(Counter Weight) 계수를 바탕으로 승강기 구동에 필요한 전동기 용량을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 승강기 설계 제원")
        
        # 적재 하중 및 속도
        load_kg = st.number_input("적재 하중 (kg)", min_value=100, value=1000, step=100)
        speed_mmin = st.number_input("정격 속도 (m/min)", min_value=10, value=60, step=15)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 효율 및 계통 계수")
        
        # 균형추 계수 (통상 0.4~0.5)
        # 카와 균형추의 무게 차이에 의한 부하만 계산하기 위함
        cw_factor = st.slider("오버밸런스율 (균형추 계수)", 0.3, 0.6, 0.45, 0.05, help="카와 적재하중의 차이를 보전하는 비율입니다. 통상 0.45 적용.")
        
        # 기계 효율 및 여유율
        eff = st.slider("종합 효율 (%)", 50, 95, 80) / 100.0
        safety_factor = st.slider("설계 여유율 (K)", 1.0, 1.5, 1.2, 0.05)

        btn = st.button("승강기 동력 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 산출 결과")
        if btn:
            # 1. 소요 동력(P) 산출 공식 (kW)
            # P = (L * V * (1 - F) * K) / (6120 * η)
            # L: 적재하중, V: 속도(m/min), F: 균형추계수, K: 여유율, η: 효율
            
            p_required = (load_kg * speed_mmin * (1 - cw_factor) * safety_factor) / (6120 * eff)
            
            # 2. HP(마력) 변환
            p_hp = p_required / 0.746

            # --- 결과 시각화 ---
            st.success(f"✅ 필요 전동기 출력: **{p_required:.2f} kW**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("계산된 축동력", f"{p_required:.2f} kW")
            res_c2.metric("환산 마력 (HP)", f"{p_hp:.1f} HP")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **균형추(Counter Weight)의 역할:** 승강기는 카 무게와 적재 하중의 약 **{cw_factor*100:.0f}%**를 상쇄하는 균형추를 설치하여 전동기의 소요 동력을 대폭 절감합니다.
            2. **기동 토크:** 승강기는 빈번한 기동과 정지가 반복되므로 정격 출력뿐만 아니라 높은 **기동 토크**를 갖는 승강기 전용 유도전동기나 동기전동기(용량에 따라)를 선정해야 합니다.
            3. **제동 저항 및 회생:** 하강 시 또는 경부하 상승 시 전동기가 발전기 역할을 하여 에너지가 역류할 수 있으므로, 제동 저항기의 용량 검토 또는 **회생 제어 인버터** 적용이 권장됩니다.
            """)
            
            st.latex(r"P [kW] = \frac{L \cdot V \cdot (1 - F) \cdot K}{6120 \cdot \eta}")
            
            
        else:
            st.info("좌측에 승강기 사양을 입력하여 필요 동력을 산출하십시오.")