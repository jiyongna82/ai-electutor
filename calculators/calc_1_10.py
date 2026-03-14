import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-10. 허용 접촉전압(Touch) 및 보폭전압(Step) 산출")
    st.caption("IEEE Std 80 기준에 따라 지표면 저항률, 인체 체중, 고장 지속 시간을 고려하여 인체 안전 한계 전압을 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 인체 및 환경 조건")
        
        # 인체 체중 기준 선택 (IEEE Std 80 표준 기준)
        body_weight = st.radio("인체 체중 기준 (kg)", [50, 70], index=0, horizontal=True, help="통상 보수적인 설계를 위해 50kg 기준을 적용합니다.")
        
        # 지표면 마감재 및 저항률 설정
        surface_material = st.selectbox(
            "지표면 마감 재질", 
            ["일반 토양", "자갈 (Crushed Rock)", "콘크리트", "아스팔트"],
            index=1
        )
        
        # 재질별 표준 저항률(Ω·m) 매핑
        rho_s_defaults = {"일반 토양": 100, "자갈 (Crushed Rock)": 2500, "콘크리트": 100, "아스팔트": 10000}
        rho_s = st.number_input("표면층 저항률 (Ω·m)", value=rho_s_defaults[surface_material], step=100)

        st.markdown("---")
        st.markdown("#### ⚡ 2. 계통 고장 조건")
        # 고장 지속 시간 (보호계전기 및 차단기 동작 시간 합계)
        t_fault = st.number_input("고장 지속 시간 (sec)", min_value=0.01, max_value=2.0, value=0.5, step=0.05)

        btn = st.button("안전 한계 전압 산출 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 안전 전압 분석 결과")
        if btn:
            # 1. 체중별 비례 상수 k 결정 (IEEE Std 80)
            k = 0.116 if body_weight == 50 else 0.157
            
            # 2. 허용 보폭전압 (E_step) 산출
            # E_step = (1000 + 6 * Cs * rho_s) * (k / sqrt(t))
            # Cs(표면층 보정계수)는 계산 편의상 1.0으로 가정 (보수적 접근)
            e_step = (1000 + 6 * rho_s) * (k / math.sqrt(t_fault))
            
            # 3. 허용 접촉전압 (E_touch) 산출
            # E_touch = (1000 + 1.5 * Cs * rho_s) * (k / sqrt(t))
            e_touch = (1000 + 1.5 * rho_s) * (k / math.sqrt(t_fault))

            # --- 결과 출력 ---
            st.success(f"✅ 분석 완료: {surface_material} 마감 조건")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("허용 보폭전압 (Step)", f"{e_step:.1f} V")
            res_c2.metric("허용 접촉전압 (Touch)", f"{e_touch:.1f} V")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **보폭전압(Step Voltage):** 지표면 전위 경도가 형성된 구간에서 양발(약 1m) 사이의 전위차입니다. 변전소 바닥에 고저항 재질인 **자갈({rho_s} Ω·m)**을 포설하여 인체를 통해 흐르는 전류를 억제합니다.
            2. **접촉전압(Touch Voltage):** 사고 전류가 흐르는 구조물과 발이 닿는 지표면 사이의 전위차입니다. 보폭전압에 비해 허용 한계치가 낮아(**{e_touch:.1f}V**) 더 위험하므로 접지 설계 시 최우선 검토 대상입니다.
            3. **안전성 확보:** 계산된 허용 전압보다 사고 시 발생하는 실제 전위 상승(GPR)이 낮도록 접지 저항을 낮추거나 차단 시간(**{t_fault}s**)을 단축하여 안전성을 확보해야 합니다.
            """)
            
            st.latex(r"E_{step} = (1000 + 6 \rho_s) \frac{k}{\sqrt{t_s}} \quad [V]")
            st.latex(r"E_{touch} = (1000 + 1.5 \rho_s) \frac{k}{\sqrt{t_s}} \quad [V]")

            
        else:
            st.info("좌측에 지표면 조건과 고장 시간을 입력하여 안전 전압 한계를 확인하십시오.")