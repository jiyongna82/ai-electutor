import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-5. 접지선(보호도체) 굵기 산출 및 검토")
    st.caption("KEC 규정에 근거하여 상도체 굵기에 따른 표준 선정 방식과 단시간 고장전류에 의한 정밀 계산 방식을 통해 최적의 접지선 규격을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 설계 및 선로 조건")
        
        # 산출 방식 선택
        calc_mode = st.radio("산출 방식 선택", ["상도체 굵기 기준 (표준법)", "고장전류 기준 (정밀식)"], horizontal=True)
        
        if calc_mode == "상도체 굵기 기준 (표준법)":
            st.info("💡 KEC 142.3.2 표에 의한 선정 방식입니다.")
            phase_wire_sq = st.select_slider(
                "상도체(Phase) 굵기 (SQ)",
                options=[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300],
                value=25.0
            )
            # 재질 선택
            material = st.selectbox("접지선 재질", ["구리 (Copper)", "알루미늄 (Aluminum)"], index=0)
        
        else:
            st.info("💡 단시간 고장전류에 의한 열적 제한 검토 방식(단열 공식)입니다.")
            i_fault = st.number_input("예상 지락 고장전류 (A)", min_value=100.0, value=5000.0, step=500.0)
            t_fault = st.number_input("차단기 차단 시간 (sec)", min_value=0.01, max_value=5.0, value=0.1, step=0.05)
            
            # K 계수 선택 (절연체 및 재질별 상수)
            k_factor = st.selectbox(
                "K 계수 (재질 및 절연체별 상수)",
                options=[143, 115, 159, 105],
                format_func=lambda x: {
                    143: "구리 / XLPE, EPR (143)", 
                    115: "구리 / PVC (115)", 
                    159: "구리 / 나전선 (159)", 
                    105: "알루미늄 / PVC (105)"
                }[x],
                index=0
            )

        btn = st.button("접지선 규격 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 접지선 설계 분석 결과")
        if btn:
            recommended_sq = 0.0
            SQ_LIST = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
            
            # --- [1] 상도체 기준 선정 로직 (KEC 142.3.2) ---
            if calc_mode == "상도체 굵기 기준 (표준법)":
                if phase_wire_sq <= 16:
                    raw_sq = phase_wire_sq
                elif phase_wire_sq <= 35:
                    raw_sq = 16
                else:
                    raw_sq = phase_wire_sq / 2
                
                # 표준 규격 매칭
                recommended_sq = next((x for x in SQ_LIST if x >= raw_sq), SQ_LIST[-1])

            # --- [2] 정밀 계산식 로직 (단열 공식) ---
            else:
                # S = (sqrt(I^2 * t)) / k
                calc_sq = (math.sqrt(i_fault**2 * t_fault)) / k_factor
                recommended_sq = next((x for x in SQ_LIST if x >= calc_sq), SQ_LIST[-1])
                st.write(f"- 계산된 최소 필요 단면적: **{calc_sq:.2f} mm²**")

            # --- 결과 출력 ---
            st.success(f"✅ 권장 접지선(보호도체) 굵기: **{recommended_sq} SQ**")
            
            st.markdown("##### 📏 설계 기준 요약")
            st.write(f"- 산출 방식: **{calc_mode}**")
            if calc_mode == "상도체 굵기 기준 (표준법)":
                st.write(f"- 적용 기준: KEC 142.3.2 (상도체 {phase_wire_sq}SQ 대응)")
            else:
                st.write(f"- 적용 수식: 단열 공식 (I={i_fault}A, t={t_fault}s)")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **KEC 142 규정:** 보호도체는 상도체 굵기에 따라 선정하거나, 고장전류의 열적 강도를 고려한 계산식에 의해 선정할 수 있습니다.
            2. **기계적 강도:** 보호도체가 케이블의 일부가 아니거나 외함에 포함되지 않은 경우, 최소 굵기는 구리 기준 **2.5SQ(보호장치 유)** 또는 **4SQ(보호장치 무)** 이상이어야 합니다.
            3. **선택적 최적화:** 지락 고장전류가 제한되는 계통(예: 저항 접지 방식)에서는 정밀 계산식을 활용하여 경제적인 접지선 설계를 할 수 있습니다.
            """)
            
            st.latex(r"S = \frac{\sqrt{I^2 \cdot t}}{k}")
            
            
        else:
            st.info("좌측에서 설계 조건을 입력한 후 분석 버튼을 눌러주세요.")