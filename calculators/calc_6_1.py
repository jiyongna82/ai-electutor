import streamlit as st
import pandas as pd
from datetime import datetime

def run_calc():
    # 1. 실시간 시점 자동 감지
    now = datetime.now()
    current_m = now.month
    current_y = now.year

    st.subheader(f"📊 6-1. FMS 기반 실시간 PUE 및 권역별 효율 분석")
    st.caption(f"현재 {current_y}년 {current_m}월의 권역별 기상 데이터를 반영하여 데이터센터 에너지 효율을 진단합니다.")

    # [데이터베이스] 권역별 월평균 기온 (℃) - 광역 단위 평년값
    regional_temp_db = {
        "서울/경기": [ -2.4, 0.5, 6.3, 12.9, 18.7, 23.1, 25.8, 26.3, 21.6, 15.0, 7.3, -0.1 ],
        "강원": [ -4.1, -0.8, 5.1, 12.1, 18.2, 22.7, 25.4, 25.6, 20.3, 13.0, 5.6, -1.5 ],
        "충청": [ -1.0, 1.8, 7.4, 13.8, 19.4, 23.6, 26.3, 26.7, 21.9, 15.1, 7.9, 0.9 ],
        "경상": [ 0.2, 2.7, 8.3, 14.7, 20.1, 24.1, 26.8, 27.3, 22.4, 15.9, 8.8, 1.9 ],
        "전라": [ 0.6, 2.3, 7.2, 13.2, 18.6, 22.8, 26.1, 26.5, 22.0, 15.6, 9.1, 2.8 ],
        "제주": [ 6.1, 6.8, 9.4, 14.1, 18.2, 21.6, 25.5, 27.1, 23.9, 19.1, 13.5, 8.3 ]
    }

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 실시간 수배전 계측 (kW)")
        total_pwr = st.number_input("센터 총 수전 전력 (Total Power)", value=3500, step=100)
        it_load = st.number_input("IT 장비 총 부하 (IT Load)", value=2500, step=100)
        
        non_it_pwr = max(0, total_pwr - it_load)
        
        st.markdown("---")
        st.markdown("#### 🌍 2. 분석 권역 설정")
        # 서울/경기를 디폴트(index=0)로 설정
        selected_region = st.selectbox("대상 권역 선택", list(regional_temp_db.keys()), index=0)
        
        avg_temp = regional_temp_db[selected_region][current_m - 1]
        st.success(f"📅 **현재 분석 시점:** {current_m}월 / **권역 평균 기온:** {avg_temp} ℃")

        st.markdown("---")
        st.markdown(f"#### ⚖️ 3. Non-IT 부하 배분 (잔여: {non_it_pwr} kW)")
        
        # 동적 동기화 슬라이더
        c_pwr = st.select_slider(
            "냉방 설비 비중 조절 (슬라이더를 움직여 배분하십시오)",
            options=list(range(0, non_it_pwr + 1, 10)),
            value=int(non_it_pwr * 0.85)
        )
        e_pwr = non_it_pwr - c_pwr
        
        # 슬라이더 폭에 맞춘 실시간 용량 동기화 표시
        st.markdown(f"""
            <div style="width: 100%; display: flex; justify-content: space-between; background-color: #f1f3f5; padding: 15px; border-radius: 10px; border: 1px solid #ced4da; margin-top: 10px;">
                <div style="text-align: left;">
                    <span style="color: #007bff; font-weight: bold; font-size: 0.85em;">❄️ 냉방 설비 전력</span><br>
                    <span style="font-size: 1.4em; font-weight: bold; color: #343a40;">{c_pwr:,} kW</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: #495057; font-weight: bold; font-size: 0.85em;">💡 기타 설비 전력</span><br>
                    <span style="font-size: 1.4em; font-weight: bold; color: #343a40;">{e_pwr:,} kW</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        btn = st.button("실시간 에너지 효율 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {selected_region} 권역 {current_m}월 분석 리포트")
        if btn:
            current_pue = total_pwr / it_load if it_load > 0 else 0
            cooling_ratio = (c_pwr / total_pwr) * 100
            
            # 외기 온도 기준 정밀 판정
            if avg_temp <= 7.0:
                mode, status = "Full Free Cooling", "최적 (Best)"
                advice = "외기 온도가 낮아 냉동기 가동 없이 100% 프리쿨링이 가능한 최적의 시기입니다."
            elif avg_temp <= 16.0:
                mode, status = "Partial Free Cooling", "양호 (Good)"
                advice = "부분 프리쿨링과 냉동기 혼합 운전 시기입니다. 냉각수 수온 최적화에 집중하십시오."
            else:
                mode, status = "Mechanical Cooling", "주의 (Chiller Run)"
                advice = "외기 온도가 높아 터보냉동기 중심 운전이 불가피합니다. 서버실 차폐 상태를 점검하십시오."

            res_df = pd.DataFrame([
                {"항목": "실시간 PUE 지수", "수치": f"{current_pue:.3f}", "상태": "📊 산출"},
                {"항목": "냉방 전력 비중", "수치": f"{cooling_ratio:.1f} %", "상태": "❄️ 분석"},
                {"항목": "현재 냉방 모드", "수치": mode, "상태": status},
                {"항목": "IT 부하 전력", "수치": f"{it_load:,} kW", "상태": "🖥️ 고정"}
            ])
            
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            st.metric(f"현재 {current_m}월 실시간 PUE", f"{current_pue:.3f}")

            st.markdown("---")
            st.markdown(f"##### 💡 전문가 운영 인사이트 ({selected_region})")
            st.success(f"**[현시점 권고사항]**\n\n{advice}")
            
            st.info(f"""
            1. **계절성 반영:** {selected_region}의 {current_m}월 평균 기온({avg_temp}℃) 기준, 현재 냉방 모드는 **{mode}**가 가장 경제적입니다.
            2. **PUE 관리:** IT 부하({it_load}kW) 대비 냉방 비중이 {cooling_ratio:.1f}%입니다. 냉방 전력을 절감할수록 PUE는 1.0에 근접합니다.
            3. **비상 대응:** 현재 설정된 냉방 수온(18℃)과 버퍼탱크 용량을 고려하여, 정전 시 충분한 백업 골든타임을 확보하고 있는지 상시 점검하십시오.
            """)
            
            
        else:
            st.info(f"권역을 선택하면 **{current_m}월**의 기상 데이터를 기반으로 즉시 분석 준비가 완료됩니다.")