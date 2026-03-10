import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-1. 3상 유도전동기 기동전류 및 기동 방식 분석")
    st.caption("표준 유도전동기의 제원과 기동 방식에 따른 기동 전류 및 토크 변화를 시뮬레이션하여 최적의 기동 설계를 지원합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전동기 기본 제원")
        
        # 계통 전압 선택
        v_sys = st.selectbox("계통 전압 (V)", [220, 380, 440, 3300, 6600], index=1)
        
        # 전동기 정격 용량 (kW)
        motor_kw = st.number_input("전동기 정격 출력 (kW)", min_value=0.1, value=37.0, step=1.0)
        
        # 기동 방식 선택
        start_method = st.selectbox(
            "기동 방식 선택",
            ["직입 기동 (Full Voltage)", "Y-△ 기동 (Star-Delta)", "리액터 기동 (65% Tap)", "소프트 스타터", "인버터 (VFD)"],
            index=1
        )
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 상세 기동 파라미터")
        # 기동 배수 (정격 대비 몇 배인가? 표준 6배)
        start_factor = st.slider("직입 기동 시 전류 배수 (표준 5~8배)", 4.0, 9.0, 6.0, 0.5)
        
        # 효율 및 역률
        motor_eff = st.slider("전동기 효율 (%)", 70, 98, 92) / 100.0
        motor_pf = st.slider("전동기 역률 (%)", 70, 100, 85) / 100.0

        btn = st.button("기동 특성 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 기동 특성 분석 결과")
        if btn:
            # 1. 정격 전류 (In) 계산
            # P = sqrt(3) * V * I * eff * pf
            i_rated = (motor_kw * 1000) / (math.sqrt(3) * v_sys * motor_eff * motor_pf)
            
            # 2. 기동 방식별 감쇄 계수 (표준 이론치)
            reduction_map = {
                "직입 기동 (Full Voltage)": 1.0,
                "Y-△ 기동 (Star-Delta)": 1/3, # 0.333
                "리액터 기동 (65% Tap)": 0.65**2, # 전압 제곱 비례인 경우 0.42
                "소프트 스타터": 0.45, # 가변적이나 초기 설정치 가정
                "인버터 (VFD)": 0.15   # 저속 기동으로 정격 수준 유지
            }
            reduction_factor = reduction_map[start_method]
            
            # 3. 최종 기동 전류 (Is)
            i_start = i_rated * start_factor * reduction_factor
            
            # 4. 기동 토크 배수 (직입 기동 시 토크 대비 비율)
            # 유도전동기 토크는 인가 전압의 제곱에 비례
            torque_ratio = reduction_factor 

            # --- 결과 시각화 ---
            st.success(f"✅ 기동 방식: **{start_method}**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("정격 전류 (In)", f"{i_rated:.1f} A")
            res_c2.metric("예상 기동 전류 (Is)", f"{i_start:.1f} A")
            
            st.write(f"- 기동 전류 감쇄 배수: **{reduction_factor:.2f}**")
            st.write(f"- 기동 토크 유지율: **{torque_ratio * 100:.1f} %** (직입 대비)")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **전압 강하 검토:** 대용량 전동기 기동 시 계통 전압 강하가 **10~15%**를 초과하지 않도록 기동 방식을 선정하십시오.
            2. **Y-△ 기동 주의점:** 기동 전류를 1/3로 줄일 수 있으나, 기동 토크 역시 1/3로 줄어듭니다. 펌프나 팬과 같이 초기 부하 토크가 낮은 부하에 적합합니다.
            3. **VFD(인버터) 활용:** 기동 전류 억제와 속도 제어가 동시에 필요한 경우 가장 우수한 솔루션입니다. 기동 전류를 정격 전류 수준 내외로 제어할 수 있습니다.
            4. **보호 협조:** 산출된 기동 전류(**{i_start:.1f}A**)와 기동 시간을 바탕으로 보호계전기의 **열적 과부하 곡선(ANSI 49/51)**과 간섭이 없는지 확인하십시오.
            """)
            
            st.latex(r"I_{rated} = \frac{P_{kW} \times 1000}{\sqrt{3} \times V \times \eta \times cos\phi}")
            st.latex(r"I_{start} = I_{rated} \times \text{Multiplier}_{start} \times \text{Factor}_{method}")
        else:
            st.info("좌측에 전동기 사양과 기동 방식을 입력한 후 분석을 실행하세요.")