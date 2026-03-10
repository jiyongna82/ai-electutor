import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("⚡ 5-1. 비상발전기 용량 산출 및 최적 병렬 구성 제언")
    st.caption("총 부하량에 따른 개별 발전기 정격과 리던던시(N+1, 2N) 컨셉에 맞는 최적의 병렬 시스템을 제안합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 부하 및 설계 컨셉")
        # 1. 유효전력 합계 (슬라이더 형식, 500kW ~ 20,000kW)
        p_total = st.slider("부하 유효전력 합계 (kW)", min_value=500, max_value=20000, value=3000, step=500)
        
        # 2. 리던던시 컨셉 선택
        redundancy = st.selectbox("신뢰성 구성 방식 (Redundancy)", 
                                  ["N+1 (일반 데이터센터 표준)", "2N (최고 등급 보안)", "단일 구성 (비용 절감형)"])
        
        # 3. 부하 성격 프리셋
        load_preset = st.selectbox("부하 구성 성격", ["데이터센터 (UPS 위주)", "일반 빌딩", "플랜트"])
        
        # 프리셋 자동 세팅
        def_eff, def_pf = (0.92, 0.90) if "데이터센터" in load_preset else (0.85, 0.82)
        
        c1, c2 = st.columns(2)
        eff = c1.number_input("부하 효율", value=def_eff)
        pf = c2.number_input("부하 역률", value=def_pf)
        
        safety_factor = st.slider("설계 여유율 (%)", 10, 30, 15)
        
        btn = st.button("병렬 시스템 최적화 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 발전기 구성 추천 리포트")
        if btn:
            # 기본 필요 용량 계산 (kVA)
            base_kva = (p_total / (eff * pf)) * (1 + safety_factor / 100)
            
            # 병렬 구성 로직 (경제적 관점에서 2000kVA~3000kVA 단위를 기준으로 분할)
            # 대형 데이터센터에서 가장 가성비 좋은 유닛은 보통 2000~2500kW(DCC 정격) 급입니다.
            unit_size_options = [1000, 1500, 2000, 2500, 3000]
            # 적정 유닛 선정 (전체 용량을 3~5대 정도로 나눌 수 있는 사이즈 선택)
            unit_size = min(unit_size_options, key=lambda x: abs(x - (base_kva / 3)))
            
            n_count = math.ceil(base_kva / unit_size)
            
            if redundancy == "N+1 (일반 데이터센터 표준)":
                total_units = n_count + 1
                total_capacity = total_units * unit_size
                desc = f"1대의 예비기(+1)를 두어 유지보수 중 정전에도 대응 가능한 안정적인 구성입니다."
            elif redundancy == "2N (최고 등급 보안)":
                total_units = n_count * 2
                total_capacity = total_units * unit_size
                desc = f"전원 계통을 완전히 이중화(A, B)하여 물리적 손상 시에도 100% 백업이 가능합니다."
            else:
                total_units = n_count
                total_capacity = total_units * unit_size
                desc = f"여유분 없이 용량만 맞춘 구성으로, 발전기 고장 시 일부 부하 차단이 필요할 수 있습니다."

            # 결과 테이블
            res_df = pd.DataFrame({
                "항목": ["필요 총 부하(여유율 포함)", "추천 개별 단위 용량", "필요 대수 (N)", "최종 구성 대수", "시스템 총 용량"],
                "데이터": [f"{base_kva:.1f} kVA", f"{unit_size} kVA", f"{n_count} 대", f"{total_units} 대", f"{total_capacity} kVA"]
            })
            st.dataframe(res_df, hide_index=True, use_container_width=True)

            st.success(f"💡 **최종 권장안:** {unit_size}kVA급 발전기 **{total_units}대** 병렬 구성을 권장합니다.")
            
            st.markdown("---")
            st.markdown(f"##### 🛡️ {redundancy} 컨셉 상세 분석")
            st.info(f"""
            - **운용 전략:** {desc}
            - **경제성 검토:** 단일 {base_kva:.0f}kVA 엔진보다 {unit_size}kVA급 병렬 구성이 부하 분담 효율 및 예비 부품 확보 면에서 유리합니다.
            - **실무 팁:** 5대 이상 병렬 시에는 동기 투입 시간(Synchronizing Time) 단축을 위해 **Dead Bus Closure(무전압 투입)** 기술 적용을 검토하십시오.
            """)

            
            st.latex(r"S_{system} = (N + R) \times S_{unit} \geq S_{load} \times (1 + \text{Margin})")
        else:
            st.info("부하 규모와 리던던시 컨셉을 선택하면 최적의 병렬 대수가 산출됩니다.")