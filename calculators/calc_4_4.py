import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-4. 고조파(Harmonics) 함유율(THD) 및 기기 영향 분석")
    st.caption("차수별 고조파 성분을 분석하여 THD를 산출하고, 지배적인 고조파 차수에 따른 맞춤형 권고 사항을 제공합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 고조파 전류 측정 데이터")
        i_fundamental = st.number_input("기본파 전류 (I1, A)", min_value=1.0, value=100.0, step=10.0)
        
        st.write("📊 **차수별 고조파 전류 (A)**")
        i3 = st.number_input("제3고조파 (I3)", min_value=0.0, value=5.0, step=0.1)
        i5 = st.number_input("제5고조파 (I5)", min_value=0.0, value=15.0, step=0.1)
        i7 = st.number_input("제7고조파 (I7)", min_value=0.0, value=7.0, step=0.1)
        i11 = st.number_input("제11고조파 (I11)", min_value=0.0, value=3.0, step=0.1)
        i13 = st.number_input("제13고조파 (I13)", min_value=0.0, value=2.0, step=0.1)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 분석 기준 설정")
        thd_limit = st.slider("관리 목표 THD (%)", 3.0, 20.0, 5.0, 0.5)

        btn = st.button("고조파 정밀 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 고조파 진단 결과 및 권고")
        if btn:
            # 1. THD 및 K-Factor 산출
            harmonics_list = {"3rd": i3, "5th": i5, "7th": i7, "11th": i11, "13th": i13}
            i_rms_harmonics = math.sqrt(sum(v**2 for v in harmonics_list.values()))
            thd_pct = (i_rms_harmonics / i_fundamental) * 100
            
            # K-Factor 계산
            k_factor = 1 + sum(((v/i_fundamental)**2 * int(k.replace('rd','').replace('th',''))**2) for k, v in harmonics_list.items())

            # 2. 지배적 고조파 판별 (가장 큰 성분 찾기)
            dominant_harmonic = max(harmonics_list, key=harmonics_list.get)
            dominant_val = harmonics_list[dominant_harmonic]

            # --- 결과 출력 ---
            if thd_pct <= thd_limit:
                st.success(f"✅ 계통 품질 양호 (THD: {thd_pct:.2f}%)")
            else:
                st.error(f"❌ 계통 품질 관리 필요 (THD: {thd_pct:.2f}%)")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("종합 왜형률 (THD)", f"{thd_pct:.2f} %")
            res_c2.metric("추정 K-Factor", f"{k_factor:.2f}")

            # 3. 차수별 맞춤 권고 사항 (핵심 업데이트)
            st.markdown("---")
            st.markdown(f"##### 📢 지배적 고조파({dominant_harmonic})에 따른 권고")
            
            advice = ""
            if dominant_harmonic == "3rd" and dominant_val > (i_fundamental * 0.05):
                advice = """
                - **원인:** PC, LED 등 단상 비선형 부하 과다 사용.
                - **영향:** 중성선에 고조파가 중첩되어 **중성선 과열 및 화재 위험**이 있습니다.
                - **조치:** 중성선 굵기 보강 또는 **영상분 고조파 필터(Zero-Sequence Filter)** 설치를 검토하십시오.
                """
            elif dominant_harmonic == "5th" and dominant_val > (i_fundamental * 0.05):
                advice = """
                - **원인:** 인버터(VFD), UPS 등 6펄스 전력전자 부하.
                - **영향:** **전력용 콘덴서의 직렬 공진**을 유발하여 설비 소손 위험이 큽니다.
                - **조치:** 콘덴서 앞단에 **직렬 리액터(6% 이상)** 설치를 확인하고, 심할 경우 **능동형 고조파 필터(APF)** 도입이 필요합니다.
                """
            elif dominant_harmonic == "7th" and dominant_val > (i_fundamental * 0.03):
                advice = """
                - **원인:** 대용량 정류기 및 인버터 부하.
                - **영향:** 변압기 및 전동기의 **소음, 진동, 손실 증가**를 유발합니다.
                - **조치:** 부하 분산 운영 또는 12펄스 정류 방식 채택을 검토하십시오.
                """
            else:
                advice = "지배적인 특정 고조파 성분이 미미하며, 전체적인 THD 관리에 집중하십시오."
            
            st.warning(advice)

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **K-Factor 활용:** 현재 K-{k_factor:.1f} 수준입니다. 일반 변압기(K-1) 사용 시 고조파 열하를 고려하여 부하율을 **{100/k_factor:.1f}%** 이하로 디레이팅(De-rating) 운용하는 것이 안전합니다.
            2. **데이터센터 특성:** UPS 및 서버 파워 서플라이에서 발생하는 고조파는 전압 파형을 왜곡시켜 정밀 장비의 오동작을 유발할 수 있으므로 상시 모니터링이 중요합니다.
            """)
            
            st.latex(r"THD_I = \frac{\sqrt{I_3^2 + I_5^2 + I_7^2 + \dots}}{I_1}")
            
        else:
            st.info("고조파 전류 데이터를 입력하여 맞춤형 권고 사항을 확인하십시오.")