import streamlit as st
import math

def run_calc():
    # 제목을 입력 변수의 성격에 맞춰 직관적으로 수정
    st.subheader("⚡ 3-7. 기동 임피던스에 따른 전압강하 및 계통 안정성 검토")
    st.caption("선로의 길이와 굵기(임피던스)를 바탕으로 전동기 기동 시의 순시 전압강하를 산출하고, 계통의 운전 신뢰성을 판정합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 기동 데이터")
        v_sys = st.selectbox("계통 전압 (V)", [220, 380, 440, 3300, 6600], index=1)
        motor_kw = st.number_input("전동기 정격 출력 (kW)", min_value=0.1, value=55.0, step=1.0)
        
        start_method = st.selectbox("기동 방식", ["직입 기동 (6배)", "Y-△ 기동 (2배)", "소프트스타터 (3배)"], index=0)
        start_factor = 6.0 if "직입" in start_method else (2.0 if "Y-△" in start_method else 3.0)
        
        st.markdown("---")
        # 입력 변수인 길이와 굵기를 '선로 임피던스 조건'으로 그룹화
        st.markdown("#### ⚙️ 2. 선로 임피던스 조건 (전압강하 변수)")
        length = st.number_input("선로 길이 (m)", min_value=1.0, value=150.0, step=10.0, help="길이가 길수록 임피던스가 증가하여 전압강하가 커집니다.")
        wire_sq = st.select_slider("적용 전선 굵기 (SQ)", options=[6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240], value=50.0, help="굵기가 굵을수록 임피던스가 감소하여 전압강하가 줄어듭니다.")

        btn = st.button("임피던스 및 전압 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 판정 결과")
        if btn:
            # 1. 기동 전류(Is) 산출
            i_rated = (motor_kw * 1000) / (math.sqrt(3) * v_sys * 0.9 * 0.85)
            i_start = i_rated * start_factor
            
            # 2. 선로 임피던스에 의한 전압강하 산출 (KEC 정수 30.8 적용)
            drop_v = (30.8 * i_start * length) / (1000 * wire_sq)
            drop_pct = (drop_v / v_sys) * 100
            
            # 3. 판정 로직
            is_safe = drop_pct <= 15.0 

            if is_safe:
                st.success(f"✅ 판정: **안전 (강하율 {drop_pct:.2f}%)**")
            else:
                st.error(f"❌ 판정: **설계 보완 필요 (강하율 {drop_pct:.2f}%)**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("기동 돌입 전류", f"{i_start:.1f} A")
            res_c2.metric("전압강하(V)", f"{drop_v:.1f} V")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **임피던스와 전압강하:** 전동기 분기 회로의 **길이({length}m)**와 **굵기({wire_sq}SQ)**는 선로 임피던스를 결정하는 핵심 요소입니다. 이 임피던스가 클수록 기동 시 전압강하가 심화됩니다.
            2. **계통 안정성:** 기동 시 전압이 급격히 떨어지는 현상은 동일 모선(Bus)을 공유하는 타 부하의 릴레이 트립이나 제어반의 오작동을 유발할 수 있습니다.
            3. **대책:** 전압강하가 과다할 경우, 임피던스를 줄이기 위해 전선을 굵게 하거나 기동 전류 자체를 줄이는 기동 방식 변경이 필요합니다.
            """)
            
            st.latex(r"e(Voltage \ Drop) = \frac{30.8 \cdot I_{start} \cdot L}{1000 \cdot A}")
            
        else:
            st.info("조건을 입력하여 임피던스 기반 전압 분석을 진행하십시오.")