import streamlit as st
import math

def run_calc():
    st.subheader("🛡️ 2-10. 차단기 간 보호협조 및 선택차단 분석")
    st.caption("상위 ACB와 하위 MCCB 간의 트립 특성을 비교하여, 사고 시 계통의 부분 정전(선택차단) 가능성을 검토합니다.")

    # 1. 입력부와 출력부를 가로로 분할
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 차단기 트립 설정")
        # [상위 차단기]
        st.markdown("**[상위] Main ACB**")
        m_at = st.number_input("Main 정격전류 (AT)", min_value=100, value=2000, step=100)
        
        c1, c2 = st.columns(2)
        m_st_set = c1.number_input("단한시(ST) 픽업 (x AT)", min_value=1.5, value=5.0, step=0.5)
        m_st_time = c2.selectbox("단한시 지연시간 (sec)", [0.1, 0.2, 0.3, 0.4, 0.5], index=2)

        st.markdown("---")
        # [하위 차단기]
        st.markdown("**[하위] Branch MCCB**")
        b_at = st.number_input("Branch 정격전류 (AT)", min_value=10, value=250, step=10)
        b_inst_set = st.number_input("순시(INST) 트립 (x AT)", min_value=2.0, value=10.0, step=1.0)
        
        st.markdown("---")
        # [사고 조건]
        st.markdown("#### ⚡ 2. 고장 시뮬레이션")
        fault_current = st.slider("예상 단락 고장 전류 (A)", 100, 30000, value=8000, step=500)

        # 기존처럼 결과 확인 버튼 유지
        btn = st.button("보호협조 정밀 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 리포트")
        # 버튼을 눌렀을 때만 결과가 출력되도록 설정
        if btn:
            # 트립 전류 기준값 계산
            m_st_i = m_at * m_st_set
            b_inst_i = b_at * b_inst_set
            
            # 판정 로직
            is_branch_trip = fault_current >= b_inst_i
            is_main_trip = fault_current >= m_st_i
            
            # 1. 고장 전류 메트릭
            st.info(f"입력된 사고 전류: **{fault_current:,.0f} A**")
            
            # 2. 비교 차트 대용 메트릭
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("하위 순시 동작점", f"{b_inst_i:,.0f} A")
            c_res2.metric("상위 단한시 동작점", f"{m_st_i:,.0f} A")

            st.divider()

            # 3. 전문가 판정 결과
            if is_branch_trip and not is_main_trip:
                st.success("✅ **보호협조 성공 (선택차단)**")
                st.write("하위 차단기만 동작 범위에 해당합니다. 상위 ACB는 동작하지 않아 정전 사고가 해당 부하에만 국한됩니다.")
            elif is_branch_trip and is_main_trip:
                st.warning("⚠️ **주의: 보호협조 중첩 (정전 확산 리스크)**")
                st.write(f"상/하위 차단기가 동시에 트립 명령을 받는 구간입니다. 상위 ACB의 **{m_st_time}초 지연** 시간 동안 하위 MCCB가 고장을 확실히 제거해야 합니다.")
            elif not is_branch_trip and not is_main_trip:
                st.info("💡 **정상 범위:** 고장 전류가 설정된 트립 값보다 작습니다.")
            else:
                st.error("❌ **설정 부적합: 상위 우선 차단 위험**")
                st.write("상위 설정치가 하위보다 낮게 설정되어 있어, 사고 시 전체 정전이 발생할 확률이 매우 높습니다.")

            st.markdown("#### 💡 실무 엔지니어링 팁")
            st.write("""
            * **ACB 단한시(ST) 설정:** 데이터센터 메인은 하위 사고 파급을 막기 위해 0.2~0.3초 정도의 지연 시간을 주는 것이 필수입니다.
            * **TCC 곡선 검토:** 계산 수치 외에도 제조사에서 제공하는 시간-전류 특성 곡선(TCC)의 공차(Tolerance) 범위를 반드시 확인하십시오.
            """)
            
            
            
        else:
            # 버튼을 누르기 전 가이드 메시지
            st.info("좌측에 차단기 트립 설정값과 예상 고장 전류를 입력한 후 **[보호협조 정밀 분석 실행]** 버튼을 클릭해 주세요.")
            st.write("---")
            st.write("※ 본 툴은 다른 페이지 이동 시 입력값이 자동으로 초기화됩니다.")