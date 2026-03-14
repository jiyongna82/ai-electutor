import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-9. 전동기 효율 및 슬립(Slip) 분석")
    st.caption("전동기의 동기 속도와 실측 회전수를 비교하여 슬립을 산출하고, 소비 전력 대비 기계적 출력의 효율을 진단합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 명판 및 측정 데이터")
        freq = st.radio("전원 주파수 (Hz)", [50, 60], index=1, horizontal=True)
        poles = st.selectbox("전동기 극수 (P)", [2, 4, 6, 8, 12], index=1)
        measured_rpm = st.number_input("실측 회전수 (rpm)", min_value=1, value=1745, step=5)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 소비전력 및 출력 데이터")
        v_in = st.number_input("측정 전압 (V)", min_value=100, value=380, step=10)
        i_in = st.number_input("측정 전류 (A)", min_value=0.1, value=25.0, step=1.0)
        pf = st.slider("측정 역률 (%)", 50, 100, 85) / 100.0
        output_kw = st.number_input("정격 출력 (kW)", min_value=0.1, value=15.0, step=1.0)

        btn = st.button("효율 및 슬립 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 진단 결과")
        if btn:
            # 1. 동기 속도(Ns) 산출
            ns = (120 * freq) / poles
            # 2. 슬립(s) 산출
            slip = (ns - measured_rpm) / ns
            # 3. 입력 전력(Pin) 산출
            p_in = (math.sqrt(3) * v_in * i_in * pf) / 1000.0
            # 4. 운전 효율(η) 산출
            current_efficiency = (output_kw / p_in) * 100 if p_in > 0 else 0

            # 결과 시각화
            st.success(f"✅ 분석 완료: 슬립 {slip*100:.2f} %")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("동기 속도 (Ns)", f"{int(ns)} rpm")
            res_c2.metric("측정 효율 (η)", f"{current_efficiency:.1f} %")
            
            if slip <= 0.05:
                st.info("💡 슬립 판정: **정상** (범위 내 운전)")
            else:
                st.warning("⚠️ 슬립 판정: **주의** (부하 과다 검토 필요)")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info("""
            1. **슬립(Slip)의 의미:** 유도전동기는 고정자 자계보다 느리게 회전해야 토크가 발생하며, 부하가 커질수록 슬립은 증가합니다.
            2. **효율 최적화:** 전동기는 정격 부하의 75~80%에서 최고 효율을 보입니다.
            """)
            
            # 수식 표기법 수정 (오류 발생 지점)
            st.latex(r"N_s = \frac{120f}{P}")
            st.latex(r"s = \frac{N_s - N}{N_s} \times 100 [\%]")
            st.latex(r"\eta = \frac{P_{out}}{\sqrt{3} \cdot V \cdot I \cdot \cos\phi} \times 100 [\%]")
            
            
        else:
            st.info("데이터를 입력하고 분석 버튼을 눌러주세요.")