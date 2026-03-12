import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🔥 6-6. VESDA 조기 화재 감지 농도 및 시퀀스 분석")
    st.caption("공기 흡입형 감지기의 단계별 연기 농도(Obs/m)를 분석하여 방재 연동 시나리오를 진단합니다.")

    # [데이터베이스] VESDA 표준 경보 설정치 (Obs/m)
    # 기술적 표준치 기준: Alert(0.05%), Action(0.08%), Fire1(0.1%), Fire2(0.2%)
    
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 실시간 감지 농도 입력")
        # 연기 농도 입력 (공기 중 감광율 % Obs/m)
        current_obs = st.number_input("현재 계측 농도 (% Obs/m)", 
                                     value=0.005, min_value=0.0, max_value=2.0, format="%.4f",
                                     help="VESDA는 아주 미세한 감광율(0.005~2.0)을 정밀 계측합니다.")
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 단계별 Threshold 설정 (표준값)")
        # 데이터센터 표준 시나리오 기반 설정
        v_alert = st.number_input("Alert 단계 (%)", value=0.05, format="%.2f")
        v_action = st.number_input("Action 단계 (%)", value=0.08, format="%.2f")
        v_fire1 = st.number_input("Fire 1 단계 (%)", value=0.10, format="%.2f")
        v_fire2 = st.number_input("Fire 2 단계 (%)", value=0.20, format="%.2f")

        btn = st.button("화재 연동 시퀀스 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 단계별 신호 전송 및 제어 상태")
        if btn:
            # --- 단계별 판정 로직 ---
            if current_obs >= v_fire2:
                status, level = "🔴 Fire 2 (위험)", 4
                action_msg = "가스 소화설비 솔레노이드 동작 신호 연동. 즉각 대피 및 자동 소화 개시."
            elif current_obs >= v_fire1:
                status, level = "🟠 Fire 1 (화재)", 3
                action_msg = "수신기 예비신호 수신 및 지구경종 송출. 운영자 현장 확인 필수."
            elif current_obs >= v_action:
                status, level = "🟡 Action (조치)", 2
                action_msg = "공조 설비(FWU/냉동기) 연동 정지 검토 및 유지보수 인원 대기."
            elif current_obs >= v_alert:
                status, level = "🔵 Alert (주의)", 1
                action_msg = "비정상 미세 입자 감지. 서버실 내 분진 발생 여부 모니터링."
            else:
                status, level = "🟢 Normal (정상)", 0
                action_msg = "안정적인 공기질 유지 중."

            # 시퀀스 데이터프레임 구성
            res_data = {
                "경보 단계": ["Alert", "Action", "Fire 1", "Fire 2"],
                "설정 농도": [f"{v_alert}%", f"{v_action}%", f"{v_fire1}%", f"{v_fire2}%"],
                "시스템 연동": ["FMS 알람", "운영자 호출", "지구경종/예비신호", "가스 소화 동작"],
                "현재 도달": ["✅" if level >=1 else "-", "✅" if level >=2 else "-", "✅" if level >=3 else "-", "✅" if level >=4 else "-"]
            }
            
            st.dataframe(
                pd.DataFrame(res_data),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "경보 단계": st.column_config.TextColumn("경보 단계", width="small"),
                    "설정 농도": st.column_config.TextColumn("설정 농도", width="small"),
                    "시스템 연동": st.column_config.TextColumn("시스템 연동", width="medium")
                }
            )

            st.metric("현재 감지 상태", status, delta=f"{current_obs:.4f} % Obs/m")

            st.markdown("---")
            st.markdown("##### 💡 운영 전문가 대응 가이드")
            
            if level >= 3:
                st.error(f"**[비상 상황]** {action_msg}")
            elif level >= 1:
                st.warning(f"**[확인 요망]** {action_msg}")
            else:
                st.success(f"**[안전]** {action_msg}")

            st.info(f"""
            1. **Fire 1단계 연동:** 수신기에 예비신호로 입력되며 실질적인 경보(지구경종)가 송출되는 시점입니다.
            2. **Fire 2단계 연동:** 최후의 단계로, 실제 가스 소화제 방출을 위한 솔레노이드 밸브 동작 신호와 연동되어 있습니다.
            3. **조기 감지의 이점:** VESDA는 일반 감지기보다 약 1,000배 이상 민감하여 전선 피복이 과열되는 단계에서 화재를 감지, 전원 차단 등의 선제적 조치를 가능케 합니다.
            """)
            
            
        else:
            st.info("실시간 연기 농도를 입력하여 센터 내 화재 연동 시퀀스를 점검하십시오.")