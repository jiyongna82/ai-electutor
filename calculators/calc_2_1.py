import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-1. 변압기 정격 용량 정밀 산출")
    st.caption("부하별 설비 용량과 수용률을 바탕으로 필요한 변압기 용량을 계산하고, 최적의 표준 정격을 추천합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 부하 데이터 입력")
        load_it = st.number_input("IT 서버 부하 (kW)", min_value=0.0, value=500.0, step=50.0)
        df_it = st.slider("IT 부하 수용률 (%)", 10, 100, 100, 5) / 100.0
        
        load_hvac = st.number_input("냉방/공조 부하 (kW)", min_value=0.0, value=300.0, step=50.0)
        df_hvac = st.slider("공조 부하 수용률 (%)", 10, 100, 70, 5) / 100.0
        
        load_etc = st.number_input("기타/전등 부하 (kW)", min_value=0.0, value=50.0, step=10.0)
        df_etc = st.slider("기타 부하 수용률 (%)", 10, 100, 60, 5) / 100.0

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 설계 계수 설정")
        pf = st.slider("종합 역률 (%)", 70, 100, 90, 1) / 100.0
        future_margin = st.slider("미래 증설 여유율 (%)", 0, 50, 20, 5) / 100.0
        
        btn = st.button("변압기 용량 산출 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 용량 산출 리포트")
        if btn:
            max_p = (load_it * df_it) + (load_hvac * df_hvac) + (load_etc * df_etc)
            total_kva = max_p / pf
            required_kva = total_kva * (1 + future_margin)
            
            TR_RATINGS = [100, 200, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 7500, 8000, 9000, 10000]
            recommended_kva = next((x for x in TR_RATINGS if x >= required_kva), TR_RATINGS[-1])

            st.success(f"✅ 권장 변압기 정격: **{recommended_kva:,.0f} kVA**")
            
            st.markdown("##### 📏 상세 산출 내역")
            st.write(f"- 합성 최대 유효전력: **{max_p:.2f} kW**")
            st.write(f"- 계산된 피상전력: **{total_kva:.2f} kVA**")
            st.write(f"- 여유율 적용 후 필요량: **{required_kva:.2f} kVA**")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 설계 가이드")
            
            # [수정 포인트] 값 사이에 "~"를 넣고 천단위 콤마를 적용하여 가독성 해결
            low_eff = recommended_kva * 0.5
            high_eff = recommended_kva * 0.7
            
            st.info(f"""
            1. **수용률(Demand Factor):** 모든 부하가 동시에 최대 출력으로 운전되지 않음을 고려한 계수입니다.
            2. **부하율 관리:** 변압기는 정격의 **{low_eff:,.0f} ~ {high_eff:,.0f} kVA (50~70%)** 구간에서 운전될 때 가장 효율이 좋습니다.
            3. **데이터센터 특이사항:** 서버실용 변압기는 IT 부하의 고조파를 고려하여 K-Factor 변압기를 사용하며, 현재 탭은 통상 4번 또는 7번을 사용합니다.
            """)
            
            st.latex(r"Tr_{kVA} = \frac{\sum (Load \times Demand \ Factor)}{pf} \times (1 + Margin)")
        else:
            st.info("좌측에 부하별 용량과 설계 조건을 입력한 후 분석 버튼을 눌러주세요.")