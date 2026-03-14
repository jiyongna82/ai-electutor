import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-5. 전동기 토크 및 출력 상호 변환 분석")
    st.caption("전동기의 회전 속도와 출력 데이터를 바탕으로 토크를 산출하거나, 요구 토크에 필요한 전동기 용량을 역산합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변환 모드 선택")
        # 계산 방향 선택
        calc_mode = st.radio(
            "계산 항목 선택", 
            ["출력(kW) → 토크(N·m) 산출", "토크(N·m) → 출력(kW) 역산"], 
            horizontal=True
        )
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 데이터 입력")
        
        # 공통 입력: 회전수
        rpm = st.number_input("회전 속도 (rpm)", min_value=1, value=1750, step=10)
        
        if "출력(kW) → 토크(N·m)" in calc_mode:
            p_kw = st.number_input("전동기 출력 (kW)", min_value=0.1, value=11.0, step=1.0)
            target_val = p_kw
        else:
            t_nm = st.number_input("부하 토크 (N·m)", min_value=0.1, value=60.0, step=1.0)
            target_val = t_nm

        # 기계 효율 반영
        mech_eff = st.slider("기계 전달 효율 (%)", 50, 100, 95) / 100.0

        btn = st.button("동력 특성 변환 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 동력 특성 분석 결과")
        if btn:
            # 1. 물리 상수 및 변환 로직
            # P [W] = T [N.m] * ω [rad/s]
            # ω = 2 * π * N / 60
            
            if "출력(kW) → 토크(N·m)" in calc_mode:
                # T = (P * 60) / (2 * π * N)
                # 1 kW = 1000 W
                res_torque = (p_kw * 1000 * 60) / (2 * math.pi * rpm) * mech_eff
                res_kgm = res_torque / 9.80665
                res_hp = p_kw / 0.746
                
                st.success(f"✅ 산출 토크: **{res_torque:.2f} N·m**")
                
                c1, c2 = st.columns(2)
                c1.metric("토크 (kgf·m)", f"{res_kgm:.2f} kgf·m")
                c2.metric("마력 (HP)", f"{res_hp:.1f} HP")
                
            else:
                # P = (T * 2 * π * N) / (60 * 1000)
                res_kw = (t_nm * 2 * math.pi * rpm) / (60 * 1000 * mech_eff)
                res_hp = res_kw / 0.746
                
                st.success(f"✅ 필요 출력: **{res_kw:.2f} kW**")
                
                c1, c2 = st.columns(2)
                c1.metric("필요 마력 (HP)", f"{res_hp:.1f} HP")
                c2.metric("각속도 (rad/s)", f"{(2*math.pi*rpm/60):.1f}")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **토크와 속도의 관계:** 전동기 출력이 일정할 때, 회전수($rpm$)가 낮아지면 토크는 비례하여 커집니다. 감속기를 사용하는 이유가 바로 여기에 있습니다.
            2. **기동 토크 고려:** 운전 중 토크 외에도 초기 정지 상태에서 부하를 움직이기 위한 **기동 토크(Starting Torque)**가 전동기 특성 곡선상에서 충분한지 반드시 확인하십시오.
            3. **VFD 운전 시 주의:** 인버터(VFD)로 저속 운전할 경우, 냉각 팬의 풍량 감소로 인한 전동기 과열이 발생할 수 있으므로 **정토크(Constant Torque)** 부하인지 **저감토크(Variable Torque)** 부하인지 구분하여 설계해야 합니다.
            4. **단위 변환:** 실무에서 혼용되는 $kgf \cdot m$ 단위는 $N \cdot m$ 값에 **9.8**을 나누어 환산합니다.
            """)
            
            st.latex(r"T [N \cdot m] = \frac{60 \times P [W]}{2\pi \times N [rpm]}")
            st.latex(r"P [kW] = \frac{T [N \cdot m] \times N [rpm]}{9550}")
            
            
        else:
            st.info("좌측에 변환할 데이터와 회전수를 입력해 주세요.")