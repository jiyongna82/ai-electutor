import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-9. 케이블 포설 장력 및 측압 계산")
    st.caption("케이블 포설 시 발생하는 견인 장력과 곡선 구간의 측압을 계산하여 케이블 피복 손상 여부를 검토합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 케이블 및 포설 경로 정보")
        w_weight = st.number_input("케이블 단위 중량 (kg/m)", min_value=0.1, value=2.5, step=0.1)
        length = st.number_input("구간 길이 (m)", min_value=1.0, value=50.0, step=5.0)
        mu = st.slider("마찰 계수 (μ)", 0.1, 1.0, 0.5, 0.05, help="전선관 내 윤활제 사용 시 0.2~0.3, 일반 0.5")

        st.markdown("---")
        st.markdown("#### 🔄 2. 곡선 구간 조건")
        r_radius = st.number_input("곡률 반경 (m)", min_value=0.5, value=1.5, step=0.1)
        theta_deg = st.number_input("곡선 각도 (degree)", min_value=0, max_value=180, value=90, step=15)

        btn = st.button("포설 안정성 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 시공 안전성 분석 결과")
        if btn:
            # 1. 직선 구간 장력 (T = μ * W * L)
            t_straight = mu * w_weight * length
            
            # 2. 곡선 구간 장력 (T_out = T_in * e^(μθ))
            theta_rad = math.radians(theta_deg)
            t_curve = t_straight * math.exp(mu * theta_rad)
            
            # 3. 측압 (P = T / R)
            side_pressure = t_curve / r_radius

            st.success(f"✅ 곡선 구간 출구 장력: **{t_curve:.2f} kgf**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("직선 구간 장력", f"{t_straight:.1f} kgf")
            res_c2.metric("최대 측압 (Pressure)", f"{side_pressure:.1f} kgf/m")

            st.markdown("---")
            st.markdown("##### 💡 전문가 시공 가이드")
            st.info(f"""
            1. **장력 제한:** 케이블 도체(구리)의 허용 인장 하중은 통상 **7kg/mm²**입니다. 산출된 장력이 이 값을 넘지 않아야 합니다.
            2. **측압 관리:** 케이블 피복 손상을 방지하기 위해 최대 측압은 일반 케이블 **300kgf/m**, 전력용 고압 케이블은 **500kgf/m** 이하로 관리하십시오.
            3. **데이터센터 시공:** DC 내 트레이 포설 시 곡률 반경(**{r_radius}m**)이 너무 작으면 측압이 급증하여 절연 성능이 저하될 수 있으므로 주의가 필요합니다.
            """)
            
            st.latex(r"T_{out} = T_{in} \cdot e^{\mu \theta}")
            st.latex(r"P = \frac{T}{R}")
            
        else:
            st.info("포설 경로 조건을 입력하여 시뮬레이션을 실행하세요.")