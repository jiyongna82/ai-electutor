import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-6. 중성선(Neutral) 굵기 산출 및 고조파 검토")
    st.caption("KEC 규정에 따라 상도체 굵기를 바탕으로 중성선 규격을 결정하고, 고조파 함유율이 높은 부하(UPS, 서버 등)에 대한 보정계수를 적용합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 상도체 및 부하 조건")
        
        # 상도체 굵기 선택
        phase_wire_sq = st.select_slider(
            "상도체(Phase) 굵기 (SQ)",
            options=[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300],
            value=70.0
        )
        
        # 부하 불평형 및 고조파 특성
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 고조파 및 환경 계수")
        thd_3rd = st.slider("제3고조파 함유율 (%)", 0, 50, 15, 5, help="데이터센터 서버 부하는 제3고조파가 N상에 중첩됩니다.")
        
        is_unbalanced = st.checkbox("부하 불평형이 심한 계통인가요?", value=False)

        btn = st.button("중성선 규격 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 중성선 설계 분석 결과")
        if btn:
            # --- [1] KEC 기본 선정 규정 ---
            # 다심케이블 또는 단심케이블 다조 포설 시 상도체와 동일 규격이 원칙
            # 단, 상도체가 16SQ(구리) 초과 시 특정 조건하에 감축 가능
            
            base_neutral_sq = phase_wire_sq
            
            # --- [2] 고조파 보정 계수 (KEC 212.4.3 관련) ---
            # 제3고조파 함유율이 15%~33% 사이일 때 보정계수 0.86 적용 등
            harmonic_factor = 1.0
            warning_msg = ""
            
            if thd_3rd > 33:
                harmonic_factor = 1.45 # 중성선 전류가 상전류보다 커지는 구간
                base_neutral_sq = phase_wire_sq * harmonic_factor
                warning_msg = "⚠️ 고조파로 인해 중성선 전류가 상전류를 초과합니다. 상도체보다 굵은 중성선 선정이 필요합니다."
            elif thd_3rd > 15:
                harmonic_factor = 1.0
                warning_msg = "💡 고조파 영향이 있으나 상도체와 동일 규격으로 수용 가능합니다."
            else:
                if phase_wire_sq > 16 and not is_unbalanced:
                    # 조건 충족 시 감축 가능성 (실무에선 데이터센터 특성상 권장하지 않음)
                    base_neutral_sq = phase_wire_sq # 데이터센터 보수적 설계 적용
            
            # 표준 규격 매칭
            SQ_LIST = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
            recommended_sq = next((x for x in SQ_LIST if x >= base_neutral_sq), SQ_LIST[-1])

            # --- 결과 출력 ---
            if thd_3rd > 33:
                st.error(f"✅ 권장 중성선 굵기: **{recommended_sq} SQ**")
            else:
                st.success(f"✅ 권장 중성선 굵기: **{recommended_sq} SQ**")
            
            if warning_msg:
                st.warning(warning_msg)

            st.markdown("##### 📏 설계 근거 요약")
            st.write(f"- 적용 상도체: **{phase_wire_sq} SQ**")
            st.write(f"- 제3고조파 함유율: **{thd_3rd} %**")
            st.write(f"- 고조파 전류 배수: **{harmonic_factor} 배**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **고조파의 영향:** 제3고조파는 각 상에서 동위상으로 중첩되어 중성선에 합산되어 흐릅니다. 함유율이 **33%**를 초과하면 중성선 전류가 상전류보다 커질 수 있습니다.
            2. **데이터센터 특수성:** 서버 부하(SMPS) 위주의 환경에서는 제3고조파 발생이 빈번하므로, 가급적 중성선을 상도체와 **1:1 비율** 이상으로 설계할 것을 권장합니다.
            3. **KEC 규정:** 상도체 굵기가 구리 16SQ를 초과하는 경우 중성선의 전류를 계산하여 감축할 수 있으나, 고조파 함유율이 **15%**를 넘는 경우에는 감축을 금지하고 있습니다.
            """)
            
            
        else:
            st.info("좌측에 상도체 규격과 고조파 함유율을 입력해 주세요.")