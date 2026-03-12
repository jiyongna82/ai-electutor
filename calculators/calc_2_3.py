import streamlit as st
import math

def run_calc():
    st.subheader("📊 2-3. 변압기 실부하 운전 효율 분석")
    st.caption("변압기 정격과 실제 측정된 부하(kW)를 비교하여 현재 운전 효율과 에너지 손실 상태를 정밀 진단합니다.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 기본 정보")
        # 표준 정격 슬라이더 (10,000kVA까지)
        tr_kva = st.select_slider(
            "변압기 정격 용량 (kVA)",
            options=[100, 200, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 7500, 8000, 9000, 10000],
            value=1000
        )
        
        eff_grade = st.radio("효율 등급", ["표준소비효율", "고효율 인증"], horizontal=True)

        # 용량별 자동 손실 추정 (표준 데이터 기반)
        if eff_grade == "고효율 인증":
            est_pi, est_pc = tr_kva * 0.0016, tr_kva * 0.0085
        else:
            est_pi, est_pc = tr_kva * 0.0021, tr_kva * 0.0105

        st.markdown("---")
        st.markdown("#### 🔌 2. 실시간 운전 데이터 입력")
        st.info("💡 현장 전력 분석기나 PMS에서 확인된 현재 수치를 입력하세요.")
        
        # [핵심] 현재 사용 부하 입력 칸
        current_load_kw = st.number_input(
            "현재 측정 부하 (kW)", 
            min_value=0.0, 
            max_value=float(tr_kva * 1.2), # 정격의 120%까지 입력 가능
            value=float(tr_kva * 0.5), # 기본값 50% 부하
            step=10.0,
            help="변압기 2차측에서 실제로 소모 중인 전력을 입력하세요."
        )
        
        pf = st.slider("운전 역률 (%)", 50, 100, 95, 1)
        
        # 미세 조정을 위한 접이식 메뉴
        with st.expander("임피던스 와트(동손) 등 상세 수정"):
            p_i = st.number_input("무부하손 (kW)", value=round(est_pi, 2), step=0.01)
            p_c = st.number_input("전부하 동손 (kW)", value=round(est_pc, 2), step=0.1)

        btn = st.button("운전 상태 정밀 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 결과 리포트")
        if btn:
            cos_theta = pf / 100.0
            
            # 1. 부하율 계산 (m = P / (kVA * cosθ))
            # 역률을 고려한 피상전력(kVA)으로 부하율 산출
            actual_kva = current_load_kw / cos_theta if cos_theta > 0 else 0
            m = actual_kva / tr_kva
            m_pct = m * 100.0
            
            # 2. 손실 및 효율 계산
            current_loss = p_i + (m**2 * p_c)
            eff = (current_load_kw / (current_load_kw + current_loss)) * 100.0 if current_load_kw > 0 else 0
            
            # 3. 최대 효율점 계산
            m_max = math.sqrt(p_i / p_c) if p_c > 0 else 0
            m_max_pct = m_max * 100.0
            
            # --- 결과 시각화 ---
            st.success(f"현재 부하율: **{m_pct:.1f} %**")
            
            # 부하율 상태바
            st.progress(min(m_pct/100.0, 1.0))
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("현재 운전 효율", f"{eff:.3f} %")
            col_res2.metric("실시간 손실 전력", f"{current_loss:,.2f} kW")
            
            st.markdown("---")
            st.markdown("#### 💡 효율 최적화 진단")
            
            # 최대 효율 지점과 비교
            diff = m_pct - m_max_pct
            st.write(f"- 이 변압기의 최고 효율 지점: 부하율 **{m_max_pct:.1f} %**")
            import streamlit as st
import math

def run_calc():
    st.subheader("📊 2-3. 변압기 실부하 운전 효율 분석")
    st.caption("변압기 정격과 실시간 사용 부하(kW)를 슬라이더로 조절하며, 부하 변동에 따른 효율 곡선과 손실 변화를 시뮬레이션합니다.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 규격 설정")
        # 1. 변압기 정격 용량 (표준 정격 슬라이더)
        tr_kva = st.select_slider(
            "변압기 정격 용량 (kVA) 선택",
            options=[100, 200, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 7500, 8000, 9000, 10000],
            value=1000
        )
        
        eff_grade = st.radio("효율 등급", ["표준소비효율", "고효율 인증"], horizontal=True)

        # 용량별 자동 손실 추정 (KEC/KS 데이터 기반)
        if eff_grade == "고효율 인증":
            est_pi, est_pc = tr_kva * 0.0016, tr_kva * 0.0085
        else:
            est_pi, est_pc = tr_kva * 0.0021, tr_kva * 0.0105

        st.markdown("---")
        st.markdown("#### 🔌 2. 실시간 사용 부하 시뮬레이션")
        
        # 2. [핵심] 측정 부하 슬라이더 (정격 용량에 따라 Max값이 자동 연동됨)
        # 과부하 운전 상황(120%)까지 테스트할 수 있도록 설정
        max_slider_kw = float(tr_kva * 1.2)
        current_load_kw = st.slider(
            "현재 사용 부하 (kW)", 
            min_value=0.0, 
            max_value=max_slider_kw, 
            value=float(tr_kva * 0.6), # 기본값 60% 설정
            step=10.0,
            help="현재 변압기에서 실제로 소모 중인 전력(kW)을 조절해 보세요."
        )
        
        pf = st.slider("운전 역률 (%)", 50, 100, 95, 1)
        
        with st.expander("임피던스 와트(동손) 등 상세 수정"):
            p_i = st.number_input("무부하손 (kW)", value=round(est_pi, 2), step=0.01)
            p_c = st.number_input("전부하 동손 (kW)", value=round(est_pc, 2), step=0.1)

        btn = st.button("운전 상태 정밀 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 실시간 운전 리포트")
        if btn or current_load_kw >= 0: # 버튼 안 눌러도 슬라이더 움직이면 바로 반영되게 설정
            cos_theta = pf / 100.0
            
            # 부하율(m) 계산
            actual_kva = current_load_kw / cos_theta if cos_theta > 0 else 0
            m = actual_kva / tr_kva
            m_pct = m * 100.0
            
            # 손실 및 효율 계산
            current_loss = p_i + (m**2 * p_c)
            eff = (current_load_kw / (current_load_kw + current_loss)) * 100.0 if current_load_kw > 0 else 0
            
            # 최대 효율점 계산
            m_max = math.sqrt(p_i / p_c) if p_c > 0 else 0
            m_max_pct = m_max * 100.0

            # 결과 시각화
            if m_pct > 100:
                st.error(f"⚠️ **위험: 과부하 운전 중 ({m_pct:.1f}%)**")
            elif m_pct > 80:
                st.warning(f"🔔 **주의: 고부하 운전 중 ({m_pct:.1f}%)**")
            else:
                st.success(f"✅ **정상: 안정적 운전 중 ({m_pct:.1f}%)**")
            
            # 부하율 게이지
            st.progress(min(m_pct/120.0, 1.0))
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("실시간 운전 효율", f"{eff:.3f} %")
            col_res2.metric("전력 손실량", f"{current_loss:,.2f} kW")
            
            st.markdown("---")
            st.markdown("#### 🎯 에너지 최적화 진단")
            
            # 효율 곡선상의 위치 분석
            st.write(f"- 이 변압기의 최고 효율 지점: 부하율 **{m_max_pct:.1f} %**")
            
            #  
            # 효율 곡선 그래프 상의 위치를 텍스트로 설명
            diff = m_pct - m_max_pct
            if abs(diff) < 5:
                st.info("🌟 **최적 상태:** 최대 효율 지점 근처에서 매우 경제적으로 운전되고 있습니다.")
            elif diff < 0:
                st.info(f"📉 **부하 부족:** 최적점 대비 부하가 적습니다. 무부하손(철손) 절감을 위해 뱅크 통합을 검토하세요.")
            else:
                st.warning(f"📈 **부하 과다:** 최적점을 초과했습니다. 부하 분산이나 변압기 증설(Bank 추가)을 검토하세요.")

            # 비용 환산
            annual_cost = current_loss * 8760 * 150 
            st.markdown(f"""
            > **연간 손실 비용 추정:** > 현재 부하율로 1년(8,760시간) 운전 시 예상되는 전력 손실액은 약 **{annual_cost/10000:,.0f} 만원**입니다.  
            > *(평균 단가 150원/kWh 적용 기준)*
            """)
            if abs(diff) < 5:
                st.info("✅ **베스트 드라이버:** 현재 최대 효율 구간 내에서 아주 경제적으로 운전 중입니다.")
            elif diff < 0:
                st.warning(f"📉 **저부하 운전 중:** 최고 효율점보다 약 {abs(diff):.1f}% 낮게 사용 중입니다. 무부하손(철손) 비중이 커서 에너지 단가가 높습니다.")
            else:
                st.error(f"📈 **고부하 운전 중:** 최고 효율점보다 약 {diff:.1f}% 높게 사용 중입니다. 동손에 의한 열 발생이 증가하고 있습니다.")

            # 연간 비용 환산 (실감나는 수치)
            annual_cost = current_loss * 24 * 365 * 150 # 150원 기준
            st.markdown(f"""
            > **경제성 분석:** > 현재 부하 상태로 1년 운전 시, 열로 사라지는 전력량은 약 **{current_loss * 8760:,.0f} kWh**이며, 
            > 비용으로 환산하면 약 **{annual_cost/10000:,.0f} 만원**입니다.
            """)
        else:
            st.info("정격 용량과 현재 사용 중인 kW 부하를 입력하고 진단 버튼을 누르세요.")