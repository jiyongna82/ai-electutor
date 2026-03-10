import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-11. 부스덕트(Busduct) 규격 및 허용전류 산출")
    st.caption("시스템 전압과 도체 재질, 환경 보정 계수를 적용하여 부스덕트의 적정 정격 전류를 산출하고 설계 타당성을 검토합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 시스템 및 설치 조건")
        
        # 시스템 전압 등급 선택
        sys_volt = st.selectbox("전압 등급", ["저압 (380V/220V)", "고압 (6.6kV)", "특고압 (22.9kV)"], index=0)
        
        # 도체 재질 선택
        material = st.radio("도체 재질", ["구리 (Copper)", "알루미늄 (Aluminum)"], horizontal=True)
        
        # 부하 전류 입력
        load_current = st.number_input("설계 최대 부하 전류 (A)", min_value=100.0, value=1600.0, step=100.0)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 환경 및 부하 특성 계수")
        
        # 주위 온도 보정 (표준 기준 온도 40℃)
        amb_temp = st.slider("주위 온도 (℃)", 20, 60, 40, 5, help="주위 온도가 40℃를 초과하면 허용전류가 감소(De-rating)합니다.")
        
        # 고조파 영향 여부
        harmonic_impact = st.checkbox("고조파 발생 부하(비선형 부하) 비중 높음", value=False)

        btn = st.button("부스덕트 정격 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 부스덕트 설계 분석 결과")
        if btn:
            # --- 전문가 선정 로직 ---
            # 1. 온도 보정 계수 (k1)
            # 도체 허용 온도 105℃, 기준 주위 온도 40℃ 기준
            if amb_temp > 40:
                k1 = math.sqrt((105 - amb_temp) / (105 - 40))
            else:
                k1 = 1.0
            
            # 2. 고조파 보정 계수 (k2)
            # 중성선 과열 및 표피효과 고려 (표준적인 0.85 적용)
            k2 = 0.85 if harmonic_impact else 1.0
            
            # 3. 필요 정격 전류 계산 (I_req)
            required_rating = load_current / (k1 * k2)
            
            # 4. 표준 정격 매칭 (Feeder/Plug-in Busway 공용 표준)
            STD_RATINGS = [400, 600, 800, 1000, 1200, 1600, 2000, 2500, 3200, 4000, 5000, 6300]
            recommended_rating = next((x for x in STD_RATINGS if x >= required_rating), STD_RATINGS[-1])

            # --- 결과 시각화 ---
            st.success(f"✅ 권장 부스덕트 정격: **{recommended_rating} A**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("필요 최소 정격", f"{required_rating:.1f} A")
            res_c2.metric("합성 보정계수", f"{k1 * k2:.2f}")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **배전 방식의 장점:** 부스덕트는 케이블 배선 대비 공간 점유가 적고 임피던스가 낮아 전압 강하 억제에 유리합니다.
            2. **온도 관리:** 대전류가 흐르는 접속부(Joint)는 열화 발생 가능성이 가장 높습니다. 적외선 열화상 진단을 통한 정기적인 온도 모니터링이 필수적입니다.
            3. **고조파 고려:** IT 장비나 인버터 부하가 많은 환경에서는 제3고조파로 인한 중성선 과열을 방지하기 위해 중성선 용량이 강화된(200% Neutral) 규격 선정을 검토하십시오.
            4. **설치 환경:** 수직 관통부 설치 시에는 층간 화재 확산 방지를 위한 **Fire-Stop** 처리를 반드시 수행해야 합니다.
            """)
            
            st.latex(r"I_{rating} \geq \frac{I_{load}}{k_{temp} \times k_{harm}}")
            
            
        else:
            st.info("좌측에 부하 전류와 설치 환경 조건을 입력하여 정격 분석을 진행하세요.")