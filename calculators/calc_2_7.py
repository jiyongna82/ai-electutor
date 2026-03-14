import streamlit as st
import math

def run_calc():
    st.subheader("🛡️ 2-7. NGR(중성점 접지 저항기) 정격 및 지락 특성 분석")
    st.caption("계통 전압과 지락 제한 전류를 바탕으로 NGR의 전기적 정격(Ω, kW)을 산출하고 보호계전기 협조를 위한 검출 전류를 분석합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 전압 및 제한 전류 설정")
        # 국내 표준 고압/특고압 계통 전압 선택
        v_sys = st.selectbox("계통 공칭 전압 (V)", [380, 440, 3300, 6600, 22900], index=3)
        
        # 지락 사고 시 제한하고자 하는 목표 전류 (국내 고압 계통은 통상 100A 적용)
        i_limit = st.number_input(
            "목표 지락 제한 전류 (A)", 
            min_value=1.0, 
            max_value=1000.0, 
            value=100.0, 
            step=10.0,
            help="지락 사고 발생 시 NGR을 통해 흐르게 할 최대 전류값입니다."
        )
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. NGR 정격 및 환경 조건")
        # NGR은 단시간 정격이 핵심 (10초가 표준)
        duration = st.selectbox(
            "단시간 정격 (초)", 
            [10, 30, 60, 3600], 
            index=0, 
            help="지락 전류를 견뎌야 하는 시간입니다. 보호계전기 차단 시간보다 길어야 합니다."
        )
        
        st.markdown("#### 🛡️ 3. 보호계전기(OCGR) 협조")
        # NGR 상단 CT 비 설정
        ct_primary = st.number_input("NGR 1차측 CT 정격 (A)", value=100, step=50)

        btn = st.button("NGR 정격 산출 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 NGR 설계 및 검토 결과")
        if btn:
            # --- [1] NGR 저항값(R) 산출 ---
            # R = E / I (E는 상전압)
            v_phase = v_sys / math.sqrt(3)
            r_ngr = v_phase / i_limit
            
            # --- [2] NGR 열적 용량(kW) 산출 ---
            # P = I^2 * R = V_phase * I
            p_ngr_kw = (v_phase * i_limit) / 1000.0
            
            # --- [3] 보호계전기 검출 전류 ---
            ct_ratio = ct_primary / 5.0
            ct_sec_i = i_limit / ct_ratio

            # --- 결과 시각화 ---
            st.success(f"✅ NGR 설계치: **{r_ngr:.2f} Ω / {p_ngr_kw:.1f} kW**")
            
            st.markdown("##### 📏 1. 전기적 정격 내역")
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("계산 저항값", f"{r_ngr:.2f} Ω")
            c_res2.metric("정격 용량", f"{p_ngr_kw:.1f} kW")
            
            st.write(f"- 인가 상전압 ($E$): **{v_phase:.1f} V**")
            st.write(f"- 정격 시간: **{duration} 초**")
            
            st.markdown("---")
            st.markdown("##### 🎯 2. 보호 협조 및 안전 진단")
            st.write(f"- 지락 사고 시 OCGR 유입 전류: **{ct_sec_i:.2f} A** ({ct_primary}/5A CT 기준)")
            
            # 위험 고지
            st.error(f"⚠️ **절연 주의:** 지락 시 NGR 함에는 **{v_phase/1000:.2f} kV**의 대지전압이 인가됩니다. 충분한 절연 거리 확보 및 1종 접지 시공을 확인하십시오.")

            st.markdown("#### 💡 전문가 설계 가이드")
            st.info(f"""
            1. **OCGR 정정:** 지락 제한 전류({i_limit}A)의 10~25% 수준에서 보호계전기를 정정하여 오동작을 방지하고 확실한 차단을 유도하십시오.
            2. **단시간 정격:** 데이터센터나 중요 플랜트에서는 차단기 부동작을 대비하여 통상 **10초 정격**을 적용합니다.
            3. **중성점 분리:** NGR 점검 시에는 중성점 단로기(DS)를 개방해야 하며, 반드시 전원이 차단된 상태에서 조작하십시오.
            """)
            
            # 수식 표시
            st.latex(r"R_{NGR} = \frac{V_{Line} / \sqrt{3}}{I_{Limit}}")
        else:
            st.info("좌측에 계통 전압과 목표 제한 전류를 입력하여 NGR 정격을 확인하세요.")