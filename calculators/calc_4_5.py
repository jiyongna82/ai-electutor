import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-5. 계통 임피던스 기반 정밀 전압강하 분석")
    st.caption("전선의 저항(R)과 리액턴스(X) 성분을 모두 고려하여, 역률 변화에 따른 정밀한 전압 변동을 시뮬레이션합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 및 선로 파라미터")
        v_sys = st.selectbox("선로 전압 (V)", [380, 440, 3300, 6600, 22900], index=0)
        i_load = st.number_input("부하 전류 (A)", min_value=1.0, value=200.0, step=10.0)
        pf = st.slider("부하 역률 (cosφ)", 0.50, 1.00, 0.90, 0.05)
        length = st.number_input("선로 길이 (m)", min_value=1.0, value=200.0, step=10.0)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 전선 임피던스 데이터 (km당)")
        # 고압/대용량 선로는 리액턴스 성분이 무시 불가능함
        r_unit = st.number_input("단위 저항 (R, Ω/km)", min_value=0.01, value=0.524, format="%.3f")
        x_unit = st.number_input("단위 리액턴스 (X, Ω/km)", min_value=0.01, value=0.085, format="%.3f")

        btn = st.button("정밀 임피던스 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 계통 해석 결과")
        if btn:
            # 1. 삼각함수 값 산출
            sin_phi = math.sqrt(1 - pf**2)
            
            # 2. 전로의 총 임피던스 (L 반영)
            r_total = r_unit * (length / 1000)
            x_total = x_unit * (length / 1000)
            
            # 3. 정밀 전압강하 산출 (3상 기준 벡터식)
            # e = √3 * I * (R*cosφ + X*sinφ)
            drop_v = math.sqrt(3) * i_load * (r_total * pf + x_total * sin_phi)
            drop_pct = (drop_v / v_sys) * 100

            # --- 결과 시각화 ---
            st.success(f"✅ 정밀 전압 강하량: **{drop_v:.2f} V**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("전압 강하율", f"{drop_pct:.2f} %")
            res_c2.metric("선로 리액턴스 성분", f"{x_total:.3f} Ω")
            
            st.write(f"- 수전단 전압(Phase-to-Phase): **{v_sys - drop_v:.1f} V**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **임피던스 법의 필요성:** 1단원의 간이식은 주로 저항(R) 성분만 고려합니다. 하지만 **4단원 전력 품질 분석**에서는 전선의 간격이나 배열에 따른 **리액턴스(X)** 성분이 전압강하에 미치는 영향을 반드시 포함해야 합니다.
            2. **역률의 영향:** 역률이 낮을수록($\sin\phi$가 클수록) 리액턴스에 의한 전압강하가 커집니다. 따라서 전압 품질 관리를 위해 **수전단 콘덴서**를 통한 역률 개선이 필수적입니다.
            3. **장거리 선로:** 고압 케이블이나 장거리 간선의 경우, 리액턴스 성분이 저항 성분의 10~20% 수준까지 도달하여 무시할 수 없는 전압 변동을 초래합니다.
            """)
            
            st.latex(r"e = \sqrt{3} \cdot I \cdot (R \cos\phi + X \sin\phi) \quad [V]")
            
        else:
            st.info("선로의 단위 임피던스(R, X) 값을 입력하여 정밀 해석을 진행하십시오.")