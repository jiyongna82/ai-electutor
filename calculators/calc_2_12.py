import streamlit as st
import math

def run_calc():
    st.subheader("🖥️ 2-12. K-Factor 적용 IT용 변압기 정밀 분석")
    st.caption("비선형 부하(UPS, 서버 등)에 의한 고조파 발열 영향을 분석하고, 적정 K-Factor 규격과 변압기 De-rating(용량 감소)율을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 부하 고조파 함유율 입력")
        st.info("💡 각 차수별 고조파 전류 함유율(%)을 입력하세요.")
        
        # 실무적으로 중요한 차수 위주로 구성
        ih_3 = st.number_input("3차 고조파 함유율 (%)", min_value=0.0, value=15.0, step=1.0)
        ih_5 = st.number_input("5차 고조파 함유율 (%)", min_value=0.0, value=20.0, step=1.0)
        ih_7 = st.number_input("7차 고조파 함유율 (%)", min_value=0.0, value=10.0, step=1.0)
        ih_11 = st.number_input("11차 고조파 함유율 (%)", min_value=0.0, value=5.0, step=1.0)
        ih_13 = st.number_input("13차 고조파 함유율 (%)", min_value=0.0, value=3.0, step=1.0)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 변압기 기본 정보")
        tr_kva = st.number_input("변압기 정격 용량 (kVA)", min_value=10.0, value=3000.0, step=100.0)
        
        btn = st.button("K-Factor 및 변압기 영향 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 리포트")
        if btn:
            # --- [K-Factor 계산 공식] ---
            # K = Σ (Ih^2 * h^2) / Σ (Ih^2)
            harmonics = [(1, 100), (3, ih_3), (5, ih_5), (7, ih_7), (11, ih_11), (13, ih_13)]
            
            sum_ih_sq = sum([(h[1]**2) for h in harmonics])
            sum_h_sq_ih_sq = sum([(h[0]**2 * h[1]**2) for h in harmonics])
            
            k_factor_calc = sum_h_sq_ih_sq / sum_ih_sq
            
            # --- [THD 계산] ---
            thd_i = math.sqrt(sum_ih_sq - 100**2) 
            
            # --- [변압기 De-rating 계산 (IEEE C57.110 기준 간소화)] ---
            # 고조파로 인한 추가 손실을 고려한 허용 부하율
            derating_factor = math.sqrt(1 / (1 + (0.05 * (k_factor_calc - 1)))) # 간이 모델링
            safe_kva = tr_kva * derating_factor

            # --- 결과 출력 ---
            st.success(f"✅ 산출된 K-Factor: **{k_factor_calc:.2f}**")
            
            st.markdown("##### 📊 1. 전력 품질 분석")
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("종합전류왜곡률 (THDi)", f"{thd_i:.1f} %")
            c_res2.metric("권장 K-Factor 등급", f"K-{int(math.ceil(k_factor_calc))}")
            
            st.markdown("---")
            st.markdown("##### ⚠️ 2. 변압기 용량 저감(De-rating) 분석")
            st.write(f"- 고조파 발열에 따른 용량 계수: **{derating_factor:.3f}**")
            st.metric("고조파 고려 허용 용량", f"{safe_kva:,.1f} kVA", 
                      delta=f"-{tr_kva - safe_kva:,.1f} kVA", delta_color="inverse")
            
            st.markdown("#### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **K-Factor의 의미:** 부하 전류의 고조파 성분이 변압기 권선에 일으키는 추가적인 와전류 손실을 견딜 수 있는 능력을 수치화한 것입니다.
            2. **데이터센터 표준:** 서버 부하가 많은 데이터센터에서는 통상적으로 **K-7** 이상의 변압기를 선정하며, 고조파가 극심할 경우 **K-13**을 적용합니다.
            3. **설계 반영:** 일반 변압기에 K-Factor {k_factor_calc:.1f} 수준의 부하를 걸면 과열로 수명이 급감하므로, 반드시 K-Factor 전용 변압기를 사용하거나 상기 계산된 {safe_kva:,.0f}kVA 이하로 운전해야 합니다.
            """)
            
            st.latex(r"K = \frac{\sum_{h=1}^{n} (I_h \cdot h)^2}{\sum_{h=1}^{n} I_h^2}")
            
            
        else:
            st.info("좌측에 고조파 함유율(%)을 입력한 후 분석 실행 버튼을 클릭해 주세요.")