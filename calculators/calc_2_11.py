import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-11. 전력용 콘덴서 및 역률 개선 상세 분석")
    st.caption("부하의 현재 역률을 목표 역률로 개선하기 위해 필요한 콘덴서 용량을 산출하고, 그에 따른 전력 손실 감소 및 전기요금 절감 효과를 분석합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 부하 현황 입력")
        sys_v = st.selectbox("계통 전압 (V)", [380, 440, 3300, 6600, 22900], index=0)
        p_kw = st.number_input("현재 유효 전력 (kW)", min_value=1.0, value=500.0, step=50.0)
        
        c1, c2 = st.columns(2)
        pf_now = c1.slider("현재 역률 (%)", 50, 99, 75, 1)
        pf_goal = c2.slider("목표 역률 (%)", 80, 100, 95, 1)
        
        st.markdown("---")
        st.markdown("#### 💰 2. 경제성 분석 조건")
        base_rate = st.number_input("한전 기본요금 단가 (원/kW)", value=8320, step=100)
        
        btn = st.button("역률 개선 효과 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 리포트")
        if btn:
            if pf_now >= pf_goal:
                st.warning("⚠️ 목표 역률이 현재 역률보다 높아야 개선 효과를 산출할 수 있습니다.")
            else:
                # 1. 필요 콘덴서 용량 (Qc) 계산
                # Qc = P * (tan(acos(pf_now)) - tan(acos(pf_goal)))
                phi1 = math.acos(pf_now / 100.0)
                phi2 = math.acos(pf_goal / 100.0)
                qc = p_kw * (math.tan(phi1) - math.tan(phi2))
                
                # 2. 선로 전류 감소 및 손실 저감율
                # 전류 감소비 = pf_now / pf_goal
                i_reduction_pct = (1 - (pf_now / pf_goal)) * 100
                # 손실 감소비 = 1 - (pf_now/pf_goal)^2
                loss_reduction_pct = (1 - (pf_now / pf_goal)**2) * 100
                
                # 3. 한전 기본요금 절감액 (역률 할증/할인 제도 반영)
                # 90% 기준, 1% 미달 시 0.2% 할증 / 1% 초과 시 0.2% 할인 (최대 95%까지)
                def get_pf_factor(pf):
                    if pf < 90: return (90 - pf) * 0.2  # 할증(+)
                    elif pf <= 95: return -(pf - 90) * 0.2 # 할인(-)
                    else: return -1.0 # 95% 초과도 1% 할인 고정

                factor_now = get_pf_factor(pf_now)
                factor_goal = get_pf_factor(pf_goal)
                
                monthly_saving = (p_kw * base_rate) * (factor_now - factor_goal) / 100

                # --- 결과 출력 ---
                st.success(f"✅ 필요 콘덴서 용량: **{qc:.2f} kVA (kVAr)**")
                
                st.markdown("##### 📏 1. 전기적 개선 효과")
                c_res1, c_res2 = st.columns(2)
                c_res1.metric("선로 전류 감소율", f"-{i_reduction_pct:.1f} %")
                c_res2.metric("선로 동손 감소율", f"-{loss_reduction_pct:.1f} %")
                
                st.markdown("---")
                st.markdown("##### 💰 2. 한전 요금 절감 (월간)")
                st.write(f"- 개선 전 기본요금 변동률: **{'+' if factor_now>0 else ''}{factor_now:.1f}%**")
                st.write(f"- 개선 후 기본요금 변동률: **{factor_goal:.1f}%**")
                st.metric("예상 요금 절감액", f"{int(monthly_saving):,} 원 / 월")
                
                st.markdown("#### 💡 전문가 기술 가이드")
                st.info(f"""
                1. **콘덴서 선정:** 계산된 **{qc:.1f}kVA**에 가장 근접한 상위 표준 규격을 선정하십시오.
                2. **직렬 리액터:** 제5고조파 억제를 위해 콘덴서 용량의 **6% (또는 13%)** 리액터를 직렬로 설치하여 콘덴서 과열을 방지하십시오.
                3. **설치 위치:** 역률 개선 효과를 극대화하고 선로 손실을 최소화하려면 부하의 말단(전동기 직하단 등)에 분산 설치하는 것이 가장 유리합니다.
                """)
                
        else:
            st.info("좌측에 현재 부하 상태와 목표 역률을 입력한 후 분석 버튼을 눌러주세요.")