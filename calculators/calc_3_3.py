import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-3. 전동기 차단기(MCCB) 및 EOCR 세팅치 산출")
    st.caption("전동기 용량에 적합한 보호차단기 정격을 선정하고, 기동 및 운전 특성을 고려한 EOCR의 최적 정정값을 계산합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 기본 정보")
        v_sys = st.selectbox("계통 전압 (V)", [220, 380, 440], index=1)
        motor_kw = st.number_input("전동기 정격 출력 (kW)", min_value=0.1, value=11.0, step=1.0)
        
        # 기동 특성 입력
        start_time = st.slider("기동 시간 (sec)", 1, 30, 5, help="전동기가 정격 속도에 도달할 때까지의 시간입니다.")
        motor_eff = st.slider("전동기 효율 (%)", 70, 98, 90) / 100.0
        motor_pf = st.slider("전동기 역률 (%)", 70, 100, 85) / 100.0

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 보호기기 설정")
        # 차단기 선정 배수 (KEC 및 설계 관례상 1.5~2.5배)
        mccb_factor = st.select_slider("차단기 선정 배수", options=[1.5, 2.0, 2.5, 3.0], value=2.5)
        
        btn = st.button("보호기기 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 보호계측 및 정정 결과")
        if btn:
            # 1. 정격 전류 (In) 산출
            i_rated = (motor_kw * 1000) / (math.sqrt(3) * v_sys * motor_eff * motor_pf)
            
            # 2. 차단기(MCCB) 정격 선정 (표준 정격 매칭)
            required_mccb = i_rated * mccb_factor
            MCCB_RATINGS = [15, 20, 30, 40, 50, 60, 75, 100, 125, 150, 175, 200, 225, 250, 400]
            selected_mccb = next((x for x in MCCB_RATINGS if x >= required_mccb), MCCB_RATINGS[-1])
            
            # 3. EOCR 정정값 산출
            # D-Time (기동지연시간): 기동시간보다 2~3초 여유
            d_time = start_time + 2
            # O-Time (동작시간): 과부하 시 차단 시간 (통상 5초)
            o_time = 5
            # LOAD (동작전류): 정격전류의 110~115%
            load_set = i_rated * 1.1

            # --- 결과 출력 ---
            st.success(f"✅ 권장 MCCB 정격: **{selected_mccb} AF/AT**")
            
            st.markdown("##### 📏 EOCR 정밀 정정 가이드")
            st.warning(f"📍 **LOAD (전류): {load_set:.1f} A** (정격의 110%)")
            st.info(f"📍 **D-TIME (기동): {d_time} sec** (기동시간 {start_time}s 기준)")
            st.info(f"📍 **O-TIME (동작): {o_time} sec** (표준 설정)")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **MCCB 선정 원칙:** 전동기 보호용 차단기는 기동 전류에 오동작하지 않도록 정격 전류의 **{mccb_factor}배** 수준으로 선정하는 것이 일반적입니다. 단, 간선 보호와의 협조를 확인하십시오.
            2. **EOCR LOAD 설정:** 부하의 실제 운전 전류가 정격보다 낮은 경우, 실제 측정된 운전 전류의 **110%**로 설정하는 것이 소손 방지에 더 효과적입니다.
            3. **결상 및 구속 보호:** EOCR은 과전류뿐만 아니라 결상, 역상, 구속(Lock) 보호 기능을 포함하므로, 기동 직후 운전 상태를 반드시 확인하여 세부 감도를 조정하십시오.
            4. **데이터센터/플랜트 유의사항:** 중요 부하의 경우 EOCR의 트립 접점을 직접 차단기에 연결할지, 알람으로만 사용할지 계통의 중요도에 따라 결정하십시오.
            """)
            
            st.latex(r"I_{rated} = \frac{P_{kW} \times 1000}{\sqrt{3} \times V \times \eta \times \cos\phi}")
            st.latex(r"I_{MCCB} \geq I_{rated} \times Factor_{start}")
            
            
        else:
            st.info("좌측에 전동기 사양을 입력하여 보호기기 세팅치를 확인하십시오.")