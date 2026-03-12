import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-8. 전압 등급별 서지 보호(LA/SA/SPD) 및 절연 협조")
    st.caption("특고압부터 저압까지 계통별 최적 보호 장치를 선정하고, 설치 거리에 따른 보호 유효성을 진단합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 전압 및 장치 선택")
        v_class = st.selectbox("계통 전압 등급", ["22.9kV (특고압)", "6.6kV/3.3kV (고압)", "380V/220V (저압)"], index=2)
        
        # --- 저압(SPD) 선택 시에만 세부 등급 노출 ---
        if "380V" in v_class:
            st.markdown("##### 🔍 저압 기기 범주 및 SPD 타입")
            cat_data = {
                "IV: 인입구 (주차단기)": {"Uw": 6.0, "SPD": "Type 1", "Up": 2.5},
                "III: 배전 계통 (분전반)": {"Uw": 4.0, "SPD": "Type 2", "Up": 1.5},
                "II: 부하 기기 (일반부하)": {"Uw": 2.5, "SPD": "Type 2", "Up": 1.5},
                "I: 정밀 기기 (IT/센서)": {"Uw": 1.5, "SPD": "Type 3", "Up": 1.0}
            }
            selected_cat = st.selectbox("보호 대상 범주", list(cat_data.keys()), index=1)
            u_w = cat_data[selected_cat]["Uw"]
            device_name = f"SPD ({cat_data[selected_cat]['SPD']})"
            default_up = cat_data[selected_cat]["Up"]
        
        # --- 특고압(LA) / 고압(SA) 설정 ---
        elif "22.9kV" in v_class:
            u_w, device_name, default_up = 125.0, "LA (피뢰기)", 72.0
        else:
            u_w, device_name, default_up = 60.0, "SA (서지흡수기)", 18.0

        st.info(f"📍 **{device_name}** 검토 / 기기 내전압: **{u_w}kV**")

        st.markdown("---")
        st.markdown(f"#### ⚙️ 2. {device_name} 상세 사양")
        u_p = st.number_input(f"{device_name} 제한전압 (Up, kV)", value=float(default_up), step=0.1)
        length = st.number_input("설치 거리 (L, m)", min_value=1.0, value=10.0, help="보호 장치와 기기 사이의 전선 길이")
        
        btn = st.button("통합 절연 협조 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {device_name} 보호 성능 분석")
        if btn:
            # 반사파 반영 (저압 1kV/μs, 고압 이상 10kV/μs)
            slope = 1 if "380V" in v_class else 10
            u_t = u_p + (slope * (2 * length / 150)) # v=150m/μs

            # 판정 (여유율 20%)
            is_safe = u_t < (u_w * 0.8)

            # --- 결과 출력 ---
            if is_safe:
                st.success(f"✅ **보호 성공:** {device_name}가 기기를 안전하게 보호합니다.")
            else:
                st.error(f"❌ **보호 불충분:** 도달 전압({u_t:.1f}kV)이 내전압 여유치를 초과합니다.")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("도달 전압 (Ut)", f"{u_t:.2f} kV")
            res_c2.metric("보호 여유율", f"{(u_w/u_t):.2f}배")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            if "380V" in v_class:
                st.info(f"**저압 SPD 관리:** {selected_cat} 범주에 대해 {device_name}를 선정했습니다. 저압은 반사파에 의한 전압 상승이 크므로 최대한 기기 직근(10m 이내)에 설치하는 것이 핵심입니다.")
            elif "22.9kV" in v_class:
                st.info("**특고압 LA 관리:** 뇌서지(Lightning Surge)로부터 메인 변압기를 보호합니다. 접지 인덕턴스를 줄이기 위해 리드선을 최대한 짧고 굵게 시공하십시오.")
            else:
                st.info("**고압 SA 관리:** VCB 개폐 시 발생하는 개폐 서지(Switching Surge)로부터 몰드 변압기 및 고압 전동기의 층간 절연을 보호합니다.")

            
            st.latex(r"U_t = U_p + \Delta U \leq 0.8 \times U_w")
        else:
            st.info("계통 등급을 선택하여 맞춤형 보호 전략을 시뮬레이션하십시오.")