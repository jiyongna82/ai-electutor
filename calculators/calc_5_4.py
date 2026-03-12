import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("🔋 5-4. UPS 병렬 시스템 및 배터리 자산 적정성 분석")
    st.caption("설계 권장 용량과 실제 설치 용량을 비교하고, 현재 자산 기준 실제 백업 가능 시간을 역산합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. UPS 및 부하 조건")
        c1, c2 = st.columns(2)
        unit_kva = c1.number_input("UPS 유닛 정격 (kVA)", value=500, step=100)
        num_units = c2.number_input("UPS 총 병렬 대수", min_value=1, value=3)
        load_kw_total = st.slider("전체 IT 부하 합계 (kW)", 100, 10000, 1000, step=100)
        
        st.markdown("---")
        st.markdown("#### ⏱️ 2. 축전지 기술 사양")
        battery_type = st.selectbox("축전지 종류 선정", ["납축전지 (VRLA)", "리튬인산철 (LFP)", "NCM (삼원계 고밀도)"])
        target_min = st.number_input("목표 백업 시간 (분)", value=15, step=5)
        
        st.markdown("#### 🔍 3. 현장 실사 데이터")
        installed_ah = st.number_input("현재 설치된 유닛당 배터리 용량 (Ah)", value=100, help="설치된 용량을 입력하면 실제 백업 시간을 역산합니다.")
        
        safety_margin = st.slider("보수율 (L)", 0.6, 1.0, 0.8 if "납" in battery_type else 0.9, 0.05)
        ups_eff = st.slider("인버터 효율 (%)", 90.0, 99.0, 94.0, 0.5)

        btn = st.button("배터리 시스템 정밀 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 진단 및 실제 백업 시간 판정")
        if btn:
            # --- 계산 로직 ---
            unit_load_kw = load_kw_total / num_units
            v_dc_bus = 480 
            unit_discharge_current = (unit_load_kw * 1000) / (v_dc_bus * (ups_eff / 100))
            
            # 1. 설계 기준 K값 및 필요 용량
            if "납축전지" in battery_type:
                k_target = 0.48 if target_min <= 15 else 0.60
            elif "인산철" in battery_type:
                k_target = 0.35 if target_min <= 15 else 0.42
            else: # NCM
                k_target = 0.32 if target_min <= 15 else 0.38
            
            required_ah = (1 / safety_margin) * k_target * unit_discharge_current

            # 2. 실제 백업 시간 역산 (K_actual = C_installed * L / I)
            # K값을 역산하여 대략적인 시간을 추정 (선형 보간 간소화 모델)
            actual_k = (installed_ah * safety_margin) / unit_discharge_current
            
            # K값에 따른 시간 추정 (범용 배터리 방전 특성 곡선 근사치)
            if "납축전지" in battery_type:
                actual_min = (actual_k / 0.48) * 15 if actual_k < 0.55 else (actual_k / 0.60) * 30
            else: # 리튬 계열
                actual_min = (actual_k / 0.35) * 15 if actual_k < 0.40 else (actual_k / 0.42) * 30

            # --- 결과 데이터 구성 ---
            items = [
                {"항목": "설계 필요 용량", "수치": f"{required_ah:.1f} Ah", "상태": f"기준({target_min}분)"},
                {"항목": "현재 설치 용량", "수치": f"{installed_ah} Ah", "상태": "✅ 확인"},
                {"항목": "예상 실가동 시간", "수치": f"{actual_min:.1f} 분", "상태": "⏱️ 역산 결과"}
            ]
            
            st.dataframe(pd.DataFrame(items), hide_index=True, use_container_width=True)

            # --- 종합 지표 ---
            st.metric("실제 예상 백업 시간", f"{actual_min:.1f} min", 
                      delta=f"{actual_min - target_min:.1f} min 여유" if actual_min > target_min else f"{actual_min - target_min:.1f} min 부족")

            st.markdown("---")
            st.markdown("##### 💡 전문가 종합 총평")
            
            if actual_min < target_min:
                st.error(f"**[용량 부족]** 현재 자산으로는 목표 시간({target_min}분) 대응이 불가능합니다. 실제 예상 시간은 약 **{actual_min:.1f}분**입니다.")
            else:
                st.success(f"**[용량 충분]** 설계 기준 대비 약 **{actual_min - target_min:.1f}분**의 추가 골든타임을 확보하고 있습니다.")
            
            st.info(f"""
            1. **역산 원리:** 현재 설치된 {installed_ah}Ah 용량에서 보수율({safety_margin})을 제외한 가용 에너지를 방전 전류로 나눈 값입니다.
            2. **환경 변수:** 실제 백업 시간은 축전지의 노후도(SOH)와 실내 온도에 따라 변동될 수 있으므로 주기적인 방전 시험이 필요합니다.
            3. **운영 팁:** 리튬 계열(LFP/NCM)은 방전 종지 전압까지 일정한 출력을 유지하므로 역산된 시간의 신뢰도가 납축전지보다 높습니다.
            """)
        else:
            st.info("데이터를 입력하면 설계 적정성 검토와 함께 실제 가동 시간을 산출해 드립니다.")