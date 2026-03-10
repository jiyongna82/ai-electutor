import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("📊 5-8. 고조파 함유율에 따른 발전기 손실 및 건전성 분석")
    st.caption("비선형 부하(UPS, 인버터 등)에서 발생하는 고조파가 발전기 권선 온도와 효율에 미치는 영향을 분석합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 발전기 및 부하 제원")
        gen_kva = st.number_input("발전기 정격 용량 (kVA)", value=2500, step=100)
        load_kw = st.number_input("현재 운전 부하 (kW)", value=2000, step=100)
        
        st.markdown("---")
        st.markdown("#### ⚡ 2. 고조파(Harmonics) 데이터")
        # THDi (전류 고조파 왜형률) 입력
        thdi = st.slider("전류 고조파 왜형률 (THDi, %)", 0, 50, 15, help="UPS나 정류기 부하의 특성에 따라 결정됩니다.")
        
        # 주요 고조파 차수별 비중 (간이 입력)
        st.markdown("##### 주요 차수별 함유량 (%)")
        h5 = st.number_input("5차 고조파 (역상분 영향)", value=10.0, min_value=0.0, max_value=100.0)
        h7 = st.number_input("7차 고조파 (영상분 영향)", value=5.0, min_value=0.0, max_value=100.0)
        
        # 발전기 설계 상수 (전문가용)
        k_factor_limit = st.number_input("발전기 허용 K-Factor (설계치)", value=1.2, step=0.1)

        btn = st.button("고조파 영향 정밀 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 고조파 손실 및 과열 진단 결과")
        if btn:
            # --- 계산 로직 ---
            # 1. K-Factor 산출 (간이 공식: 1 + (THDi/100)^2)
            # 실제로는 각 차수별 자승 합이나, 실무적 근사치 적용
            calc_k_factor = 1 + (thdi / 100)**2
            
            # 2. 고조파에 의한 추가 동손(Copper Loss) 비율
            # 고조파 전류는 표피효과(Skin Effect)로 인해 권선 저항을 증가시킴
            additional_loss_pct = (calc_k_factor - 1) * 100
            
            # 3. 출력 저감(Derating) 필요성 판정
            # 발전기 온도 상승은 전류의 자승에 비례하므로, K-Factor가 허용치를 넘으면 저감 필요
            derating_factor = math.sqrt(k_factor_limit / calc_k_factor) if calc_k_factor > k_factor_limit else 1.0
            recommended_max_load = gen_kva * derating_factor

            # --- 결과 데이터프레임 ---
            diag_items = [
                {"항목": "산출 K-Factor", "수치": f"{calc_k_factor:.3f}", "판정": "적정" if calc_k_factor <= k_factor_limit else "초과"},
                {"항목": "고조파 추가 손실", "수치": f"+{additional_loss_pct:.2f} %", "판정": "📊 분석"},
                {"항목": "권선 온도 상승률", "수치": f"약 {additional_loss_pct * 1.2:.1f} % 상승", "판정": "⚠️ 주의" if additional_loss_pct > 10 else "안전"},
                {"항목": "권장 최대 출력", "수치": f"{recommended_max_load:.1f} kVA", "판정": "💡 제언"}
            ]
            
            st.dataframe(pd.DataFrame(diag_items), hide_index=True, use_container_width=True)

            # --- 종합 지표 ---
            st.metric("발전기 실질 가용 용량", f"{recommended_max_load:.0f} kVA", 
                      delta=f"{recommended_max_load - gen_kva:.0f} kVA (손실반영)")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            if calc_k_factor > k_factor_limit:
                st.error(f"**[위험]** 현재 부하의 고조파 함유율이 발전기 설계 한계를 초과합니다. 권선 과열로 인한 절연 파괴 위험이 있으므로 부하 제한 혹은 필터 보강이 필요합니다.")
            else:
                st.success(f"**[안전]** 현재 고조파 수준은 발전기가 충분히 감당 가능한 범위 내에 있습니다.")

            st.info(f"""
            1. **손실 메커니즘:** 고조파 전류는 발전기 권선의 표피효과를 유발하여 유효 저항을 증가시키고, 회전자 표면에 와전류(Eddy Current)를 발생시켜 온도를 급격히 상승시킵니다.
            2. **K-Factor의 의미:** 부하 전류의 고조파 함유 정도를 나타내는 지표로, 수치가 높을수록 발전기와 변압기의 과열 위험이 큽니다.
            3. **운용 전략:** 데이터센터 비상 운전 시 UPS의 입력 필터(Active Filter 등)가 정상 작동하는지 확인하여 발전기 측으로 유입되는 THDi를 **15% 이내**로 관리하는 것이 권장됩니다.
            """)
            
            
        else:
            st.info("발전기 용량과 부하의 THDi 데이터를 입력하여 고조파 영향을 분석하십시오.")