import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-8. 단락 시 전선 열적 제한 및 허용 시간 검토")
    st.caption("단락 사고 시 흐르는 고장 전류에 의해 전선의 온도가 절연체 허용 온도에 도달하는 시간을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전선 및 단락 조건 입력")
        insulation = st.selectbox("전선 절연체 종류", ["XLPE (최종 250℃)", "PVC (최종 160℃)"], index=0)
        wire_sq = st.select_slider(
            "전선 굵기 (SQ)",
            options=[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300],
            value=25.0
        )
        
        st.markdown("---")
        st.markdown("#### ⚡ 2. 고장 전류 및 차단 특성")
        i_fault_ka = st.number_input("예상 단락 고장 전류 (kA)", min_value=0.1, value=5.0, step=0.5)
        t_actual = st.number_input("차단기 차단 시간 (sec)", min_value=0.01, max_value=5.0, value=0.1, step=0.01)

        btn = st.button("열적 제한 검토 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 판정 결과")
        if btn:
            # 변수명 통일: i_fault_a
            k = 143 if "XLPE" in insulation else 115
            i_fault_a = i_fault_ka * 1000
            
            # 허용 시간 계산 t = (k*S/I)^2
            t_allow = ((k * wire_sq) / i_fault_a)**2 if i_fault_a > 0 else 0
            # 필요 최소 굵기 역산 S = I*sqrt(t)/k
            s_min = (i_fault_a * math.sqrt(t_actual)) / k

            is_safe = t_actual <= t_allow
            
            if is_safe:
                st.success(f"✅ 판정 결과: **안전 (Safe)**")
            else:
                st.error(f"❌ 판정 결과: **위험 (Danger)**")
            
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("전선 허용 시간", f"{t_allow:.3f} s")
            c_res2.metric("실제 차단 시간", f"{t_actual:.3f} s")
            
            st.write(f"- 고장 전류 발생 시 **{t_allow:.3f}초** 내에 차단되어야 안전합니다.")
            st.write(f"- 현재 조건에서 필요한 최소 굵기: **{s_min:.2f} SQ**")
            
            st.latex(r"t = \left( \frac{k \cdot S}{I} \right)^2 \quad [s]")
        else:
            st.info("조건을 입력한 후 검토 버튼을 눌러주세요.")