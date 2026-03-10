import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-7. 지락 사고 분석: EPR 및 계통 절연 진단")
    st.caption("현장 설계 사양(NGR 등)에 따른 지락 전류를 산출하고, 운용 환경을 고려한 기술적 진단을 수행합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 및 계통 제원")
        tr_connection = st.selectbox("변압기 결선 방식", ["Delta - Wye (D-y)", "Delta - Delta (D-D)"], index=0)
        v_line = st.selectbox("2차측 상간 전압 (V)", [380, 440, 3300, 6600, 22900], index=0)
        
        tr_standards = [100, 150, 200, 300, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 5000, 7500, 10000]
        tr_kva = st.select_slider("변압기 용량 (kVA)", options=tr_standards, value=1000)
        tr_z = st.number_input("변압기 임피던스 (%Z)", min_value=1.0, value=6.0, step=0.1)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 접지 설계 파라미터")
        if tr_connection == "Delta - Delta (D-D)":
            grounding_type = "비접지 (GPT)"
        else:
            grounding_type = st.selectbox("계통 접지 방식", ["직접 접지", "저항 접지 (NGR)", "비접지 (GPT)"], index=1)
        
        r_ground = st.number_input("종합 접지저항 (Rg, Ω)", min_value=0.1, value=10.0, step=0.5)

        if grounding_type == "저항 접지 (NGR)":
            ngr_ohm = st.number_input("NGR 저항값 (Rn, Ω)", min_value=1.0, value=38.1)
        elif grounding_type == "비접지 (GPT)":
            c_val = st.number_input("계통 대지정전용량 (μF)", min_value=0.01, value=1.0)

        btn = st.button("계통 지락 정밀 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 계통 해석 및 실무 진단")
        if btn:
            v_phase = v_line / math.sqrt(3)
            z_tr = (tr_z / 100) * (v_line**2 / (tr_kva * 1000))
            
            # 1. 지락 전류(Ig) 및 전위 계수
            if grounding_type == "직접 접지":
                i_g = v_phase / math.sqrt(z_tr**2 + r_ground**2)
                k_coeff = 1.3
            elif grounding_type == "저항 접지 (NGR)":
                i_g = v_phase / (ngr_ohm + r_ground)
                k_coeff = 1.732
            else:
                i_g = 3 * (2 * math.pi * 60) * (c_val * 1e-6) * v_phase
                k_coeff = 1.732

            epr_v = i_g * r_ground
            v_healthy = v_phase * k_coeff

            # --- 실무형 통합 진단 ---
            st.markdown("##### 📍 종합 진단 의견")
            
            # 설계 적정성
            if grounding_type == "저항 접지 (NGR)":
                st.success(f"🛡️ **설계 타당성: 양호 (전류 제한 계통)**")
                st.write(f"- NGR 설계치를 통해 사고 전류를 **{i_g:.1f}A** 수준으로 안정적으로 관리 중입니다.")
            
            # 운영 환경 및 안전성
            if epr_v <= 1000:
                st.info(f"✅ **운용 환경: 정상 (설비 보호 구역)**")
                st.write(f"- EPR({epr_v:.0f}V) 수치는 이론적 상승치이나, 폐쇄형 판넬(GIS/MCSG) 구조 및 출입 제한 구역임을 고려할 때 실질적인 감전 위험은 매우 낮습니다.")
            else:
                st.warning(f"🟡 **운용 환경: 고전위 구역 (유지관리 주의)**")
                st.write(f"- 사고 시 일시적인 전위 상승이 예상되므로, 판넬 도어 및 외함의 등전위 본딩 상태를 정기적으로 점검하십시오.")

            st.markdown("---")
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("지락 전류 (Ig)", f"{i_g:.2f} A")
            res_c2.metric("건전상 최대전위", f"{v_healthy:.1f} V")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **현장 관리 포인트:** 전위 상승보다 중요한 것은 **'등전위 본딩'**입니다. 판넬 내 모든 도체와 구조체가 하나의 전위로 묶여 있다면 사람이 판넬 내부를 조작 중이라 하더라도 전위차(Voltage Difference)가 발생하지 않아 안전합니다.
            2. **절연 협조:** 건전상 전위 상승치(**{v_healthy:.1f}V**)를 고려하여, 케이블 및 설비의 절연 내력과 SPD 선정 시 이 전압을 견딜 수 있는 규격(Uc)을 확인하십시오.
            3. **데이터센터 특성:** 경북 CDC와 같은 보안 및 전문 운영 환경에서는 직접적인 접촉 기회가 차단되어 있으므로, 공학적 수치보다는 시스템의 연속성과 절연 파괴 예방에 초점을 맞추어 관리합니다.
            """)
            
            st.latex(r"EPR = I_g \times R_g, \quad V_{healthy} = V_{phase} \times 1.732")
            
        else:
            st.info("실무 데이터를 입력하고 분석 결과를 확인하십시오.")