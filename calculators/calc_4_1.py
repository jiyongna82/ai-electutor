import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-1. 수변전계통 단락전류 및 차단용량 산출")
    st.caption("변압기 제원과 계통 임피던스를 바탕으로 3상 단락전류를 산출하고, 보호기기의 적정 차단 용량을 검토합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 및 계통 제원")
        
        # 시스템 전압 선택
        v_sys = st.selectbox("기준 전압 (V)", [220, 380, 440, 3300, 6600, 22900], index=1)
        
        # 변압기 용량 및 임피던스
        tr_kva = st.number_input("변압기 정격 용량 (kVA)", min_value=10, value=1000, step=100)
        tr_z = st.number_input("변압기 퍼센트 임피던스 (%Z)", min_value=1.0, max_value=20.0, value=6.0, step=0.1)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 상위 계통 및 여유율")
        # 한전 계통 임피던스는 보통 무시하거나 작게 설정 (보수적 계산을 위해 0 선택 가능)
        source_z = st.slider("상위 계통 임피던스 가산 (%Z)", 0.0, 2.0, 0.0, 0.1, help="상위 계통(한전 등)의 임피던스를 포함할 경우 입력합니다. 0은 무한대 모선 가정.")
        
        # 설계 여유율
        safety_factor = st.slider("차단 용량 설계 여유율", 1.0, 2.0, 1.25, 0.05)
        
        btn = st.button("단락 용량 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 계통 고장 분석 결과")
        if btn:
            # 1. 정격 전류 (In) 산출
            i_rated = tr_kva / (math.sqrt(3) * (v_sys / 1000))
            
            # 2. 합성 퍼센트 임피던스 (%Z_total)
            total_z = tr_z + source_z
            
            # 3. 3상 단락 전류 (Is) 산출
            # Is = (In * 100) / %Z
            i_short = (i_rated * 100) / total_z
            
            # 4. 단락 용량 (Ps) 산출
            p_short = (math.sqrt(3) * v_sys * i_short) / 1000 # kVA 단위
            p_short_mva = p_short / 1000 # MVA 단위
            
            # 5. 권장 차단 용량 (Interrupting Capacity)
            # 차단기는 kA 단위로 선정
            rec_ka = (i_short / 1000) * safety_factor
            
            # 표준 차단 용량 매칭 (예시)
            STD_KA = [2.5, 5, 7.5, 10, 12.5, 25, 35, 42, 50, 65, 80, 100]
            selected_ka = next((x for x in STD_KA if x >= rec_ka), STD_KA[-1])

            # --- 결과 시각화 ---
            st.success(f"✅ 예상 최대 단락전류: **{i_short/1000:.2f} kA**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("정격 전류 (In)", f"{i_rated:.1f} A")
            res_c2.metric("단락 용량 (Ps)", f"{p_short_mva:.2f} MVA")
            
            st.warning(f"📍 **권장 최소 차단 용량: {selected_ka} kA**")
            st.write(f"- 계산치({rec_ka:.2f}kA) 대비 여유율 {safety_factor}배 적용")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **단락 전류의 중요성:** 단락 사고 시 흐르는 거대한 전류는 전선과 기기에 강력한 **기계적 충격(전자력)**과 **열적 손상**을 입힙니다. 차단기는 반드시 이 전류를 안전하게 차단할 수 있는 용량을 가져야 합니다.
            2. **%Z(퍼센트 임피던스):** 변압기의 %Z가 낮을수록 전압 강하는 줄어들지만, 사고 시 단락 전류는 기하급수적으로 커집니다. 계통의 경제성과 안전성 사이의 균형이 필요합니다.
            3. **차단기 선정:** 산출된 단락 전류(**{i_short/1000:.2f} kA**)보다 큰 정격 차단 용량을 가진 기기(VCB, ACB, MCCB 등)를 선정하십시오. 용량이 부족할 경우 사고 시 차단기가 폭발할 위험이 있습니다.
            """)
            
            st.latex(r"I_s = \frac{100}{\%Z} \times I_n = \frac{100}{\%Z} \times \frac{P}{\sqrt{3}V}")
            st.latex(r"P_s = \sqrt{3} \times V \times I_s \quad [MVA]")
            
            
        else:
            st.info("변압기 사양을 입력하여 계통의 최대 고장 전류를 시뮬레이션하십시오.")