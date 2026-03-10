import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-2. 보호계전기(OCR/OCGR) 정정치 및 보호협조 분석")
    st.caption("변압기 용량과 CT 비를 바탕으로 계전기의 동작 전류(Tap)와 동작 시간(Lever)을 산출하여 최적의 보호협조 곡선을 도출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 및 CT 제원")
        tr_kva = st.number_input("보호 대상 변압기 용량 (kVA)", min_value=10, value=1000, step=100)
        v_sys = st.selectbox("전압 등급 (V)", [380, 3300, 6600, 22900], index=3)
        
        # CT비 설정 (예: 100/5)
        ct_primary = st.number_input("CT 1차 정격 (A)", min_value=1, value=40, step=5)
        ct_secondary = 5 # 표준 5A 기준
        ct_ratio = ct_primary / ct_secondary
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. OCR(과전류) 정정 파라미터")
        # 부하전류의 125~150% 정정 관례
        ocr_margin = st.slider("OCR 동작 배수 (부하전류 대비 %)", 100, 200, 150, 5) / 100.0
        
        # 계전기 특성 곡선 (IEC 표준 반한시 등)
        curve_type = st.selectbox("계전기 반한시 특성", ["NI (Normal Inverse)", "VI (Very Inverse)", "EI (Extremely Inverse)"], index=0)
        
        # 목표 차단 시간 (단락 전류 유입 시)
        target_time = st.slider("목표 차단 시간 (sec)", 0.1, 2.0, 0.6, 0.1)

        btn = st.button("계전기 정정 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 계전기 정정 및 분석 결과")
        if btn:
            # 1. 정격 전류 (In) 산출
            i_rated = tr_kva / (math.sqrt(3) * (v_sys / 1000))
            
            # 2. OCR Tap 전류 산출 (계전기 입력측 전류)
            # Tap = (In * Margin) / CT_Ratio
            ocr_tap = (i_rated * ocr_margin) / ct_ratio
            
            # 표준 Tap 값 매칭 (가장 가까운 표준값 추천)
            STD_TAPS = [2, 3, 4, 5, 6, 7, 8, 10, 12]
            recommended_tap = min(STD_TAPS, key=lambda x: abs(x - ocr_tap))
            
            # 3. Lever (Time Dial) 산출
            # NI 곡선 공식: t = Lever * (0.14 / ( (I/I_tap)^0.02 - 1 ))
            # 고장전류를 정격의 10배로 가정하여 Lever 역산
            m = 10 # 다중도 (Multiple)
            if curve_type == "NI (Normal Inverse)":
                lever = target_time / (0.14 / (pow(m, 0.02) - 1))
            elif curve_type == "VI (Very Inverse)":
                lever = target_time / (13.5 / (m - 1))
            else: # EI
                lever = target_time / (80 / (pow(m, 2) - 1))

            # --- 결과 출력 ---
            st.success(f"✅ OCR 정정 제언 (CT {ct_primary}/5 기준)")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("동작 전류 (Tap)", f"{recommended_tap} A")
            res_c2.metric("시간 배율 (Lever)", f"{lever:.2f}")
            
            st.write(f"- 변압기 정격 전류: **{i_rated:.2f} A**")
            st.write(f"- 실제 동작 1차 전류: **{recommended_tap * ct_ratio:.1f} A**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **정정 원칙:** OCR은 변압기 허용 과부하 및 기동 전류에는 동작하지 않고, 단락 사고 시에는 **상위 보호 장치(한전)보다 먼저** 혹은 **하위(ACB)보다 늦게** 동작하도록 시간차(C.T.I)를 두어야 합니다.
            2. **지락 보호(OCGR):** 지락 계전기는 통상 정격 전류의 **30% 이하** 또는 최소 Tap으로 정정하여 미세한 지락 사고를 감지하도록 설정합니다. (단, 비접지 계통은 GPT/ZCT 방식 적용)
            3. **C.T.I (Coordination Time Interval):** 상하위 차단기 간에는 약 **0.2~0.4초**의 시간 여유를 두어 사고 구간만 분리하는 '선택 차단'이 가능하게 하십시오.
            """)
            
            st.latex(r"I_{tap} = \frac{I_{rated} \times Margin}{CT_{ratio}}")
            st.latex(r"t = Lever \times \frac{0.14}{(I/I_{tap})^{0.02} - 1} \quad (NI \ Curve)")
            
            
        else:
            st.info("변압기 용량과 CT비를 입력하여 보호계전기 정정치를 시뮬레이션하십시오.")