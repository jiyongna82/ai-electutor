import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("☀️ 5-5. 태양광(PV) 발전 효율 및 수익 시뮬레이터")
    st.caption("2026년 시장 시세와 유지관리 주기를 반영하여 수익성을 분석하고 개선 방안을 제안합니다.")

    # 지역별 일사량 데이터
    region_sun_hours = {
        "서울/경기": 3.4, "강원": 3.5, "충청": 3.6, "경북": 3.8, "경남": 3.7, "전라": 3.8, "제주": 3.6
    }

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 설비 및 운용 조건")
        pv_capacity = st.number_input("태양광 설치 용량 (kW)", value=300.0, step=10.0)
        
        eff_help = """
        **시스템 종합 효율 구성 요소:**
        1. 인버터 변환 손실: 3~5%
        2. 온도 상승 저하: 10~15%
        3. 배선 및 접속함 손실: 2~3%
        4. 미스매칭 및 초기 열화: 1~2%
        *최종 합계 약 80~85%가 표준입니다.*
        """
        system_eff = st.slider("시스템 종합 효율 (%)", 70.0, 95.0, 85.0, 0.5, help=eff_help)
        
        selected_region = st.selectbox("설치 지역 선택", list(region_sun_hours.keys()), index=0)
        avg_sun_hours = region_sun_hours[selected_region]

        # 세척 주기 옵션
        cleaning_options = ["방치(연 1회 이하)", "정기점검(연 1~2회)", "분기 세척(연 4회)", "밀착 관리(매월 세척)"]
        maintenance_factor = {
            "방치(연 1회 이하)": 0.90, 
            "정기점검(연 1~2회)": 0.95, 
            "분기 세척(연 4회)": 0.98, 
            "밀착 관리(매월 세척)": 1.0
        }
        
        cleaning_cycle = st.select_slider("모듈 세척 주기 선택", options=cleaning_options, value="분기 세척(연 4회)")
        current_m_factor = maintenance_factor[cleaning_cycle]

        st.markdown("---")
        st.markdown("#### 💰 2. 수익성 파라미터 (2026 시세)")
        smp_price = st.number_input("SMP 단가 (원/kWh)", value=135.0, step=1.0)
        rec_price = st.number_input("REC 단가 (원/REC)", value=78000.0, step=100.0)
        rec_weight = st.number_input("REC 가중치", value=1.5, step=0.1)

        btn = st.button("수익 개선 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {selected_region} 발전 분석 및 개선 제언")
        if btn:
            # 1. 현재 조건 발전량 및 수익 계산
            daily_gen = pv_capacity * avg_sun_hours * (system_eff / 100) * current_m_factor
            monthly_gen = daily_gen * 30.4
            monthly_smp_rev = monthly_gen * smp_price
            rec_issuance = (monthly_gen / 1000) * rec_weight
            monthly_rec_rev = rec_issuance * rec_price
            total_rev = monthly_smp_rev + monthly_rec_rev

            # 2. 개선 제언 계산 (한 단계 더 높은 관리 주기 선택 시)
            current_idx = cleaning_options.index(cleaning_cycle)
            improvement_msg = ""
            
            if current_idx < len(cleaning_options) - 1:
                next_cycle = cleaning_options[current_idx + 1]
                next_m_factor = maintenance_factor[next_cycle]
                
                # 개선 시 기대 발전량 및 수익
                improved_daily_gen = pv_capacity * avg_sun_hours * (system_eff / 100) * next_m_factor
                improved_monthly_gen = improved_daily_gen * 30.4
                improved_total_rev = (improved_monthly_gen * smp_price) + ((improved_monthly_gen / 1000) * rec_weight * rec_price)
                
                added_revenue = improved_total_rev - total_rev
                improvement_msg = f"💡 관리 주기를 **'{next_cycle}'**로 단축할 경우, 월 약 **{added_revenue:,.0f}원**(연간 {added_revenue*12/10000:.1f}만원)의 추가 수익이 예상됩니다."
            else:
                improvement_msg = "✅ 현재 **최상(밀착 관리)** 수준으로 운영 중입니다. 효율적인 세척 비용 집행 여부를 점검하십시오."

            # 결과 데이터프레임
            items = [
                {"항목": "월간 예상 발전량", "수치": f"{monthly_gen:,.1f} kWh", "상태": "📈 산출"},
                {"항목": "월간 SMP 수익", "수치": f"{monthly_smp_rev:,.0f} 원", "상태": "💰 매각"},
                {"항목": "월간 REC 수익", "수치": f"{monthly_rec_rev:,.0f} 원", "상태": f"🌱 가중치 {rec_weight}"}
            ]
            st.dataframe(pd.DataFrame(items), hide_index=True, use_container_width=True)

            # 종합 지표
            st.metric("월 총 예상 수익 (SMP+REC)", f"{total_rev:,.0f} 원")
            
            # 개선 제언 강조 박스
            st.success(improvement_msg)

            st.markdown("---")
            st.info(f"""
            **[운용 가이드]**
            * **수익 구조:** 현재 REC 수익이 전체의 약 **{(monthly_rec_rev/total_rev)*100:.1f}%**를 차지합니다. 가중치가 높을수록 세척 관리에 따른 수익 개선 폭이 더 커집니다.
            * **관리 팁:** 데이터센터 인근 공사나 미세먼지 농도가 높은 시기에는 일시적으로 세척 주기를 단축하여 발전 효율 하락을 방어하는 것이 경제적입니다.
            """)
        else:
            st.info("지역과 설비 정보를 확인하고 분석 버튼을 눌러주세요.")