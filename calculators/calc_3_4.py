import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 3-4. 인버터(VFD) 고조파 발생량 및 필터 분석")
    st.caption("설치된 리액터(AC/DC) 종류에 따른 고조파 억제 효과를 분석하고 보완 대책을 제안합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 인버터 사양")
        vfd_kw = st.number_input("인버터 정격 용량 (kW)", min_value=0.1, value=45.0, step=1.0)
        v_sys = st.selectbox("계통 전압 (V)", [220, 380, 440], index=1)
        
        rectifier_type = st.selectbox(
            "인버터 정류 방식",
            ["6-Pulse (일반형)", "12-Pulse (저고조파형)", "Active Front End (AFE)"],
            index=0
        )

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 리액터 설치 현황")
        # 선택에 따라 결과 메시지가 가변적으로 변하도록 설정
        reactor_choice = st.radio("설치된 리액터 종류", ["AC 리액터 (입력측)", "DC 리액터 (내장형)", "둘 다 설치", "없음"], index=1)
        
        target_thdi = st.slider("목표 고조파 왜곡률(THDi) (%)", 5, 40, 15, 5)

        btn = st.button("고조파 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 결과 및 대책")
        if btn:
            # 1. 기본 전류 산출
            i_fund = (vfd_kw * 1000) / (math.sqrt(3) * v_sys * 0.95 * 0.95)
            
            # 2. 리액터 종류별 THDi 감쇄 로직
            # 6-Pulse 기준: 무필터(85%), AC만(40%), DC만(45%), 둘다(30%) 수준 추정
            if rectifier_type == "6-Pulse (일반형)":
                if reactor_choice == "AC 리액터 (입력측)": est_thdi = 40.0
                elif reactor_choice == "DC 리액터 (내장형)": est_thdi = 45.0
                elif reactor_choice == "둘 다 설치": est_thdi = 30.0
                else: est_thdi = 85.0
            elif rectifier_type == "12-Pulse (저고조파형)":
                est_thdi = 12.0
            else: # AFE
                est_thdi = 5.0
            
            i_harmonic = i_fund * (est_thdi / 100.0)

            # --- 결과 출력 최적화 ---
            st.success(f"✅ 현재 설정에 의한 예상 THDi: **{est_thdi:.1f} %**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("기본파 전류(I1)", f"{i_fund:.1f} A")
            res_c2.metric("고조파 전류(Ih)", f"{i_harmonic:.1f} A")

            # 선택한 리액터에 따른 맞춤형 가이드 출력
            if "DC 리액터" in reactor_choice:
                st.info(f"💡 **DC 리액터 운용 팁:** 내장형 DC 리액터는 AC 리액터 대비 공간 효율이 좋고 역률 개선 효과가 뛰어나지만, 전원측 서지 보호 능력은 상대적으로 낮습니다.")
            elif "AC 리액터" in reactor_choice:
                l_mh = ((v_sys / math.sqrt(3)) * 0.03) / (2 * math.pi * 60 * i_fund) * 1000
                st.info(f"💡 **AC 리액터 권장 사양:** 3% 임피던스 기준 약 **{l_mh:.3f} mH** 이상의 리액터 사용을 권장합니다.")
            
            # 목표치 미달 시 추가 제언
            if est_thdi > target_thdi:
                st.error(f"⚠️ 목표치({target_thdi}%)를 초과합니다. 능동형 필터(APF) 추가 설치를 검토하십시오.")
            else:
                st.write("✨ 현재 리액터 구성으로 고조파 관리 기준을 만족합니다.")

            st.markdown("---")
            st.markdown("##### 💡 기술 메모")
            st.info("""
            - **DC 리액터:** 인버터 내부 DC 링크에 설치되어 리플 전류를 억제하고 고조파를 저감합니다.
            - **상호 보완:** 고조파에 매우 민감한 계통이라면 AC 리액터와 DC 리액터를 혼용하여 시너지 효과를 내는 것이 좋습니다.
            """)
            
            st.latex(r"I_{total} = \sqrt{I_1^2 + I_5^2 + I_7^2 + \dots}")
        else:
            st.info("조건을 선택한 후 분석 버튼을 눌러주세요.")