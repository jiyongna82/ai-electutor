import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-10. 계통별 역률 개선 및 고조파(SR) 최적 설계")
    st.caption("부하 특성에 따른 역률 개선과 고조파 억제 대책을 통합 분석합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 및 설치 환경")
        v_class = st.selectbox("설치 위치 및 계통 전압", 
                              ["저압(380V 계통)", "저압(440V 계통)", "고압(3.3kV 계통)", "고압(6.6kV 계통)"], index=0)
        
        v_system = float(v_class.split('(')[1].split('V')[0].replace('k', '000'))
        
        # LED 부하 특성 업데이트 (역률 0.99 세팅)
        load_types = {
            "일반 유도전동기 부하": {"pf": 0.80, "main_h": "저차수(미비)", "sr_rate": 6},
            "인버터(VFD) 및 전력변환 부하": {"pf": 0.85, "main_h": "제5, 7고조파", "sr_rate": 6},
            "IT 및 서버실 (데이터센터)": {"pf": 0.95, "main_h": "제3고조파", "sr_rate": 13},
            "LED 조명 부하 (PFC 내장)": {"pf": 0.99, "main_h": "제3고조파(SMPS)", "sr_rate": 13}
        }
        selected_load = st.selectbox("주요 부하 종류 선택", list(load_types.keys()))
        load_info = load_types[selected_load]

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 부하 및 역률 데이터")
        p_kw = st.number_input("부하 유효전력 (P, kW)", min_value=1.0, value=500.0)
        
        # LED 부하 선택 시 현재 역률을 0.99(거의 1.0)으로 제언
        pf_now = st.number_input("현재 역률 (표준 자동세팅)", min_value=0.10, max_value=1.00, value=load_info['pf'])
        pf_target = st.number_input("목표 역률", min_value=0.80, max_value=1.00, value=0.95)

        btn = st.button("계통 맞춤형 설계 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 계통별 최적 설계 리포트")
        if btn:
            # 1. 필요 콘덴서 용량(Qc) 산출
            # 이미 역률이 목표보다 높을 경우를 대비한 로직
            if pf_now >= pf_target:
                qc_val = 0.0
                st.info("💡 **알림:** 현재 역률이 목표 역률보다 높으므로 추가적인 콘덴서 설치가 불필요할 수 있습니다.")
            else:
                tan_phi1 = math.tan(math.acos(pf_now))
                tan_phi2 = math.tan(math.acos(pf_target))
                qc_val = p_kw * (tan_phi1 - tan_phi2)

            # 2. 리액터(SR) 자동 결정 및 전압 상승
            sr_rate = load_info['sr_rate']
            sr_val = qc_val * (sr_rate / 100)
            v_terminal = v_system / (1 - (sr_rate / 100))
            
            # --- 결과 요약 ---
            st.success(f"✅ **설계 분석: {selected_load}**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("권장 콘덴서(SC)", f"{qc_val:.1f} kVAR")
            res_c2.metric("직렬 리액터(SR)", f"{sr_val:.1f} kVAR")
            
            st.warning(f"⚠️ **중요: 고조파 및 전압 관리**")
            if "LED" in selected_load or "IT" in selected_load:
                st.write(f"- LED/IT 부하는 역률이 높더라도 **{load_info['main_h']}** 성분이 큽니다.")
                st.write(f"- 따라서 콘덴서 용량보다는 **중성선 고조파 유입 방지**에 집중해야 하며, 리액터 설치 시 단자 전압 **{v_terminal:.1f}V**를 견디는 제품이 필수입니다.")
            
            # 전압 등급별 권장 정격
            if v_system == 380: v_rated = "440V~480V"
            elif v_system == 440: v_rated = "480V~525V"
            elif v_system == 3300: v_rated = "3,600V~3,800V"
            else: v_rated = "7,200V"
            
            st.info(f"💡 **권장 사양:** {v_system}V 계통 기준, 정격 전압 **{v_rated}** 이상 선정 권고.")

            st.markdown("---")
            st.markdown("##### 📍 실무 유지관리 포인트")
            if "LED" in selected_load:
                st.write("- **조명 부하 특이점:** 역률 개선보다는 **영상분 고조파(Zero-Sequence)** 필터링이 중요합니다. 콘덴서 설비와 리액터의 공진점이 고조파 차수와 겹치지 않도록 주의하십시오.")
            else:
                st.write(f"- **고조파 대책:** {selected_load}의 {load_info['main_h']} 공진 방지를 위해 {sr_rate}% 리액터를 매칭했습니다.")

            
            st.latex(r"Q_c = P(\tan(\arccos(PF_1)) - \tan(\arccos(PF_2)))")
        else:
            st.info("부하 특성을 선택하시면 고조파 분석과 함께 최적 전압 사양을 제언합니다.")