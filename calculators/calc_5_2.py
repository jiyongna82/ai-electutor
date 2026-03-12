import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("⚡ 5-2. 비상발전기 정밀 종합 진단 및 건전성 분석")
    st.caption("항목별 표준 기준값과 측정치를 비교하여 시스템 건전성을 즉시 판정합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 엔진 및 냉각 계통")
        c1, c2 = st.columns(2)
        coolant_temp = c1.number_input("냉각수 온도 (℃)", value=85, help="표준: 75~95℃")
        oil_press = c2.number_input("오일 압력 (kg/cm²)", value=4.5, step=0.1, help="표준: 3.5~6.0 kg/cm²")
        
        st.markdown("#### 📊 2. 시운전 성능 (Full Load)")
        load_pct = st.slider("테스트 부하율 (%)", 0, 110, 100)
        exh_temp_avg = st.number_input("배기 온도 평균 (℃)", value=480, help="표준: 400~550℃")
        exh_temp_dev = st.slider("기둥별 배기 온도 편차 (℃)", 0, 100, 15, help="표준: 50℃ 이내")
        
        st.markdown("#### ⏱️ 3. 기동 및 응답 특성")
        start_time = st.number_input("기동 후 전압 확립 시간 (sec)", value=8.5, step=0.1, help="표준: 10초 이내")
        v_dip = st.slider("순시 전압 강하량 (%)", 0, 30, 12, help="표준: 25% 이내")

        btn = st.button("종합 정밀 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 항목별 진단 판정 결과")
        if btn:
            # --- 진단 데이터 구성 및 판정 로직 ---
            items = []
            
            # 1. 냉각수 온도
            res1 = "✅ 양호" if 70 <= coolant_temp <= 98 else "🚨 불량"
            items.append({"진단 항목": "냉각수 온도", "측정값": f"{coolant_temp} ℃", "기준값": "75~95 ℃", "상태": res1})
            
            # 2. 오일 압력
            res2 = "✅ 양호" if 3.5 <= oil_press <= 6.5 else "🚨 불량"
            items.append({"진단 항목": "오일 압력", "측정값": f"{oil_press} kg/cm²", "기준값": "3.5~6.0 kg/cm²", "상태": res2})
            
            # 3. 배기 온도 편차
            res3 = "✅ 양호" if exh_temp_dev <= 50 else "🚨 불량"
            items.append({"진단 항목": "배기 온도 편차", "측정값": f"{exh_temp_dev} ℃", "기준값": "50 ℃ 이하", "상태": res3})
            
            # 4. 기동 확립 시간
            res4 = "✅ 양호" if start_time <= 10.0 else "🚨 불량"
            items.append({"진단 항목": "기동 확립 시간", "측정값": f"{start_time} sec", "기준값": "10.0 sec 이하", "상태": res4})
            
            # 5. 순시 전압 강하
            res5 = "✅ 양호" if v_dip <= 25 else "🚨 불량"
            items.append({"진단 항목": "순시 전압 강하", "측정값": f"{v_dip} %", "기준값": "25 % 이하", "상태": res5})

            # DataFrame 생성 및 인덱스 제거 출력
            res_df = pd.DataFrame(items)
            st.dataframe(res_df, hide_index=True, use_container_width=True)

            # --- 종합 점수 및 총평 ---
            error_count = sum(1 for item in items if "🚨" in item["상태"])
            health_score = max(0, 100 - (error_count * 20))
            
            st.metric("종합 건전성 점수 (G-Health Index)", f"{health_score} / 100")

            st.markdown("---")
            st.markdown("##### 💡 운영 전문가 총평")
            
            if error_count == 0:
                st.success(f"**[종합 양호]** 모든 지표가 표준 범위 내에 있습니다. 현재 부하율 {load_pct}%에서의 운전 상태는 매우 안정적입니다.")
            else:
                # 불량 항목 리스트 추출
                faulty_list = [item["진단 항목"] for item in items if "🚨" in item["상태"]]
                faulty_text = ", ".join(faulty_list)
                st.error(f"**[점검 필요]** {faulty_text} 항목에서 기준치 이탈이 감지되었습니다. 즉각적인 원인 파악을 권고합니다.")
            
            
        else:
            st.info("시운전 결과 데이터를 입력하여 발전기 계통의 이상 유무를 진단하십시오.")