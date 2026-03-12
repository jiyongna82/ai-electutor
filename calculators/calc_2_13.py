import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-13. 고압 콘덴서 NVS 보호 및 SR 전압 상승 분석")
    st.caption("고압 진상 콘덴서와 직렬 리액터(SR) 조합 시 발생하는 단자 전압 상승을 검토하고, NVS(중성점 불평형 전압) 보호 방식의 건전성을 분석합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 고압 콘덴서 및 리액터 사양")
        v_sys = st.selectbox("계통 정격 전압 (V)", [3300, 6600], index=1)
        qc_kva = st.number_input("콘덴서 정격 용량 (kVA)", min_value=10.0, value=150.0, step=10.0)
        
        # 지용 님 현장 사양인 6% 리액터(9kVA) 기준
        sr_rate = st.slider("직렬 리액터(SR) 리액턴스 비 (%)", 4.0, 15.0, 6.0, 1.0, help="일반적으로 제5고조파 억제를 위해 6% 적용")
        
        st.markdown("---")
        st.markdown("#### 🛡️ 2. NVS 보호 계통 설정")
        st.info("💡 NVS는 콘덴서 내부 소자 고장 시 중성점 간 발생하는 전위차를 감지합니다.")
        nvs_setting = st.number_input("NVS 동작 전압 설정 (V)", min_value=1.0, value=20.0, step=1.0)
        
        btn = st.button("콘덴서 설비 정밀 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 리포트")
        if btn:
            # --- [1] 직렬 리액터에 의한 전압 상승 계산 ---
            # Vc = Vs / (1 - L)  (Vs: 계통전압, L: 리액터 비율)
            v_terminal = v_sys / (1 - (sr_rate / 100.0))
            v_increase = v_terminal - v_sys
            
            # --- [2] 리액터 용량 검증 ---
            # Ql = Qc * L
            sr_kva_calc = qc_kva * (sr_rate / 100.0)
            
            # --- [3] NVS 동작 원리 가이드 ---
            # 중성점 간 전위차 시뮬레이션 (단순화된 가이드)
            
            # --- 결과 출력 ---
            st.success(f"✅ 분석 완료: {v_sys}V 계통 {sr_rate}% 리액터 적용")
            
            st.markdown("##### 📈 1. 콘덴서 단자 전압 상승")
            st.write(f"- 리액터 삽입 후 콘덴서 단자 전압: **{v_terminal:.1f} V**")
            st.write(f"- 전압 상승분: **{v_increase:.1f} V** (약 {(v_increase/v_sys)*100:.1f}%)")
            st.warning(f"⚠️ **주의:** 콘덴서의 정격 전압은 단자 전압 상승분({v_terminal:.0f}V) 이상인 제품을 선정해야 절연 파괴를 방지할 수 있습니다.")
            
            st.markdown("---")
            st.markdown("##### ⚙️ 2. 직렬 리액터(SR) 정격")
            st.write(f"- 산출된 필요 리액터 용량: **{sr_kva_calc:.2f} kVA**")
            if abs(sr_kva_calc - 9.0) < 1.0:
                st.info("💡 **현장 정합성:** 지용 님 현장의 **9kVA 리액터**는 150kVA 콘덴서의 6% 용량으로 아주 적절하게 설계되어 있습니다.")
            
            st.markdown("---")
            st.markdown("##### 🛡️ 3. NVS(Neutral Voltage Sensor) 진단")
            st.write(f"- 감시 방식: **Y-Y 결선 중성점 간 불평형 전압 검출**")
            st.write(f"- 설정치: **{nvs_setting} V**")
            st.info("""
            * **동작 원리:** 콘덴서 내부 소자가 단락되면 브리지 회로의 평형이 깨지며 중성점 사이에 전압이 발생합니다.
            * **장점:** 지락과는 별개로 콘덴서 자체의 내부 고장을 조기에 발견하여 폭발 사고를 예방할 수 있습니다.
            """)
            
            
            st.markdown("#### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **고조파 공진:** SR 6% 적용 시 제5고조파에 대해 용량성에서 유도성으로 계통 특성이 변하여 고조파 공진을 억제합니다.
            2. **AFPR 연동:** 해당 콘덴서는 자동역률제어기(AFPR)에 의해 계통 역률에 따라 차등 투입되므로, 투입 시 발생하는 돌입 전류 및 과도 현상을 상시 모니터링하십시오.
            3. **유지보수:** NVS 경보 발생 시에는 즉시 콘덴서를 개방하고 각 상의 정전용량(μF)을 측정하여 소자 이상 유무를 확인하십시오.
            """)
            
            # 수식 표시
            st.latex(r"V_c = \frac{V_s}{1 - L}")
        else:
            st.info("좌측에 고압 콘덴서 및 리액터 사양을 입력한 후 분석 버튼을 클릭하세요.")