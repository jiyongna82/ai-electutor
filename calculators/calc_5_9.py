import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🌐 5-9. 신재생 연계형 마이크로그리드 안정성 검토")
    st.caption("가동 가능한 에너지원을 선택하여 계통 분리 시 자립 운전 가능성을 진단합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 가용 에너지원 선택 및 출력")
        
        # 체크박스를 통한 에너지원 활성화 제어
        use_pv = st.checkbox("태양광(PV) 가동", value=True)
        pv_gen = st.number_input("PV 현재 출력 (kW)", value=300, step=10) if use_pv else 0
        
        use_ess = st.checkbox("ESS 배터리 가동", value=True)
        ess_dis = st.number_input("ESS 방전 출력 (kW)", value=500, step=50) if use_ess else 0
        
        use_gen = st.checkbox("비상발전기 가동", value=True)
        gen_set = st.number_input("발전기 가동 출력 (kW)", value=2000, step=100) if use_gen else 0
        
        st.markdown("---")
        st.markdown("#### ⚡ 2. 수용가 부하 조건")
        critical_load = st.number_input("최우선 필수 부하 (kW)", value=2500, step=100)
        total_load = st.number_input("전체 수용 부하 (kW)", value=3000, step=100)
        
        # 총 발전량 및 신재생 비중 계산
        total_gen = pv_gen + ess_dis + gen_set
        re_gen = pv_gen + ess_dis
        re_fraction = (re_gen / total_gen * 100) if total_gen > 0 else 0
        
        st.markdown("---")
        spinning_reserve = st.slider("운전 예비력 확보율 (%)", 0, 50, 20)

        btn = st.button("안정성 시뮬레이션 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 투입 자산 기반 자립성 진단")
        if btn:
            power_balance = total_gen - critical_load
            
            # 1. 수지 판정
            if total_gen == 0:
                balance_status = "❌ 발전원 없음"
            elif power_balance >= 0:
                balance_status = "✅ 자립 가능"
            else:
                balance_status = "🚨 용량 부족"
                
            # 2. 신재생 변동성 리스크 (발전기 관성 유무에 따른 가중치)
            if not use_gen and re_gen > 0:
                stability_risk = "🔴 극히 위험 (관성 자산 없음)"
            elif re_fraction > 40:
                stability_risk = "⚠️ 주의 (주파수 변동성 높음)"
            else:
                stability_risk = "🟢 안정 (기저 전력 확보)"

            # --- 결과 데이터프레임 (인덱스 제거) ---
            diag_results = [
                {"항목": "총 가동 발전량", "수치": f"{total_gen:,} kW", "비고": "Active Sources"},
                {"항목": "필수 부하 과부족", "수치": f"{power_balance:,} kW", "비고": balance_status},
                {"항목": "신재생 에너지 비중", "수치": f"{re_fraction:.1f} %", "비고": stability_risk},
                {"항목": "자립 가능 시간(예상)", "수치": "연속 가능" if use_gen else "ESS 잔량 의존", "비고": "📊 분석"}
            ]
            
            st.dataframe(pd.DataFrame(diag_results), hide_index=True, use_container_width=True)

            # --- 종합 지표 ---
            st.metric("마이크로그리드 자립률", f"{(total_gen / total_load * 100) if total_load > 0 else 0:.1f} %")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운영 가이드")
            if total_gen < critical_load:
                st.error(f"**[경고]** 선택된 자원만으로는 필수 부하 감당이 불가능합니다. 부족분: **{abs(power_balance):,}kW**")
            
            if not use_gen and (use_pv or use_ess):
                st.warning("발전기(회전 관성) 없이 신재생 전력만으로 운용 중입니다. 부하 변동 시 주파수 탈조 위험이 매우 높으니 정밀한 인버터 제어가 요구됩니다.")

            st.info(f"""
            1. **자원 최적화:** 현재 가동 중인 에너지원 조합으로 {balance_status} 상태입니다.
            2. **관성 제어:** 비상발전기는 시스템의 기준 전압과 주파수를 잡아주는 역할을 합니다. 가급적 발전기를 기저 전력으로 활용하십시오.
            3. **운용 전략:** 태양광 출력 급변 시 ESS가 즉각 보상할 수 있도록 유연성 자원을 상시 대기시켜야 합니다.
            """)
            
            
        else:
            st.info("좌측 체크박스에서 가용한 에너지원을 선택하여 시뮬레이션을 시작하십시오.")