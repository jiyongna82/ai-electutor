import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("🧯 6-7. 가스계 소화 밀폐도(Fan Integrity) 테스트 시뮬레이션")
    st.caption("서버실 누설 면적과 소화 가스 특성을 분석하여 법적 설계 농도 유지 시간(Retention Time)을 예측합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 방호구역 및 가스 제원")
        room_height = st.number_input("방호구역 층고 (m)", value=4.5, step=0.1)
        gas_type = st.selectbox("소화약제 종류", ["HFC-23 (할론 대체)", "IG-541 (이네르젠)", "CO2 (이산화탄소)"])
        
        st.markdown("---")
        st.markdown("#### 🔍 2. 누설 및 차압 데이터 (Door Fan Test)")
        # 누설 면적(EqLA) 입력
        leak_area = st.number_input("추정 누설 면적 (cm²)", value=150.0, step=10.0, 
                                    help="바닥 하부, 케이블 관통부, 문 틈새 등의 총 누설 면적입니다.")
        
        # 유지 기준 시간 (NFPA 2001 기준 통상 10분)
        required_time = st.slider("요구 유지 시간 (분)", 5, 20, 10)

        st.markdown("---")
        st.markdown("#### 🎯 3. 설계 농도 설정")
        design_conc = st.slider("설계 농도 (%)", 5.0, 50.0, 12.0, 0.5)

        btn = st.button("밀폐도 및 유지시간 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 소화 성능 유지 분석 리포트")
        if btn:
            # --- 간략화된 유지시간 산출 로직 (NFPA 2001 개념 모델) ---
            # 실제 공식은 유체역학적 복잡도가 높으나, 실무 시뮬레이션을 위해 선형 근사 적용
            # 유지시간은 층고에 비례, 누설면적에 반비례하는 특성을 가짐
            est_retention_time = (room_height * 500) / (leak_area * (design_conc / 10))
            
            if est_retention_time >= required_time:
                status, color = "✅ 합격 (Pass)", "green"
            else:
                status, color = "🚨 불합격 (Fail)", "red"

            # 결과 데이터프레임
            res_data = {
                "분석 항목": ["예상 유지 시간", "요구 유지 시간", "허용 누설 면적(추정)", "가스 밀도 특성"],
                "계측 데이터": [f"{est_retention_time:.1f} 분", f"{required_time} 분", f"{leak_area * 0.8:.1f} cm²", "고밀도 하부 침강"],
                "진단 결과": [status, "NFPA 기준", "보완 필요" if est_retention_time < required_time else "양호", "주의"]
            }
            
            st.dataframe(
                pd.DataFrame(res_data),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "분석 항목": st.column_config.TextColumn("분석 항목", width="medium"),
                    "계측 데이터": st.column_config.TextColumn("계측 데이터", width="small"),
                    "진단 결과": st.column_config.TextColumn("진단 결과", width="small")
                }
            )

            st.metric("예측 유지 시간 (Retention Time)", f"{est_retention_time:.1f} 분", 
                      delta=f"{est_retention_time - required_time:.1f} 분", delta_color="normal")

            st.markdown("---")
            st.markdown("##### 💡 소화설비 전문가 가이드")
            
            if status == "🚨 불합격 (Fail)":
                st.error(f"**[밀폐력 보완 시급]** 현재 누설 면적({leak_area}cm²)으로는 가스가 목표 시간 내에 하부로 빠져나갑니다. 액세스 플로어 하부 실링 및 케이블 관통부 방화 댐퍼를 점검하십시오.")
            else:
                st.success(f"**[밀폐력 양호]** 설계 농도가 {required_time}분 이상 유지될 것으로 예측됩니다. 재연소 방지 능력이 확보되었습니다.")

            

            st.info(f"""
            1. **하부 누설 주의:** 데이터센터 특성상 냉방을 위한 하부 공간(Plenum)이 많아 누설에 취약합니다. 가스는 공기보다 무거워 하부 틈새로 먼저 소실됩니다.
            2. **Retention Time의 의미:** 불꽃이 꺼진 뒤에도 가연물이 다시 발화하지 않도록 일정 농도를 유지하는 시간입니다. 
            3. **정기 점검:** VESDA(6-6)와 연동되어 조기에 화재를 감지하더라도, 물리적인 밀폐도가 뒷받침되지 않으면 가스 소화는 실패할 수 있습니다.
            """)
            
            st.latex(r"T = \frac{V}{A_{leak} \cdot \sqrt{2gH}} \cdot \ln\left(\frac{C_{initial}}{C_{final}}\right)")
        else:
            st.info("방호구역의 제원과 도어 팬 테스트 값을 입력하여 소화 가스 유지 능력을 확인하십시오.")