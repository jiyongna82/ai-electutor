import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-2. 전동기 역률 개선용 저압 진상콘덴서 선정")
    st.caption("개별 전동기 부하의 역률을 개선하기 위한 최적의 콘덴서 용량을 산출하고, 과보상 방지를 위한 설계 가이드를 제공합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 및 부하 조건")
        
        # 전동기 정격 용량 입력
        motor_kw = st.number_input("전동기 정격 출력 (kW)", min_value=0.1, value=37.0, step=1.0)
        
        # 현재 역률 및 목표 역률 설정
        curr_pf = st.slider("현재 역률 (%)", 50, 95, 85) / 100.0
        target_pf = st.slider("목표 역률 (%)", 90, 100, 95) / 100.0

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 설치 및 제어 방식")
        # 제어 방식 (전동기와 동시 투입 여부)
        control_type = st.radio("콘덴서 설치 방식", ["전동기 단자 직접 접속 (동시투입)", "MCC 반내 별도 제어"], index=0)
        
        system_volt = st.selectbox("계통 전압 (V)", [220, 380, 440], index=1)

        btn = st.button("콘덴서 용량 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 콘덴서 용량 분석 결과")
        if btn:
            # 1. 필요 콘덴서 용량(Qc) 산출 공식
            # Qc = P * (tanθ1 - tanθ2)
            theta1 = math.acos(curr_pf)
            theta2 = math.acos(target_pf)
            
            qc_calc = motor_kw * (math.tan(theta1) - math.tan(theta2))
            
            # 2. 과보상 한계치 체크 (전동기 무부하 전류의 90% 수준 권장)
            # 일반적인 유도전동기 무부하 전류는 정격의 약 25~30% 가정
            i_rated = (motor_kw * 1000) / (math.sqrt(3) * system_volt * curr_pf * 0.9) # 효율 0.9 가정
            i_no_load = i_rated * 0.3
            qc_limit = (math.sqrt(3) * system_volt * i_no_load) / 1000.0

            # --- 결과 시각화 ---
            st.success(f"✅ 산출된 필요 콘덴서 용량: **{qc_calc:.2f} kVAR**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("목표 역률 도달 시", f"{target_pf*100:.0f} %")
            res_c2.metric("자기여자 한계치", f"{qc_limit:.2f} kVAR")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **용량 선정 원칙:** 콘덴서 용량은 전동기 무부하 시의 피상전력(kVA)보다 작아야 합니다. 과보상 시 전동기 차단 후 잔류 전하에 의한 **자기여자 현상(Self-Excitation)**으로 단자 전압이 상승하여 절연 파괴를 초과할 수 있습니다.
            2. **설치 위치:** 전동기 단자에 직접 접속할 경우 전동기 기동 시 콘덴서가 같이 투입되는 구조입니다. 이 경우 선로 전체의 전류가 감소하여 전압 강하 개선 효과가 극대성됩니다.
            3. **역률 개선 효과:** 역률을 개선하면 변압기 및 배선 선로의 전력 손실($I^2R$)이 감소하며, 설비 용량의 여유분(kVA)이 증대됩니다.
            4. **고조파 주의:** 인버터(VFD)를 사용하는 전동기에는 단자에 직접 콘덴서를 설치하지 마십시오. 인버터 출력측 고조파와 콘덴서가 공진을 일으켜 설비 사고를 유발할 수 있습니다.
            """)
            
            st.latex(r"Q_c = P \times (\tan\theta_1 - \tan\theta_2) \quad [kVAR]")
            
            
        else:
            st.info("좌측에 전동기 사양과 목표 역률을 입력하여 필요한 콘덴서 용량을 확인하십시오.")