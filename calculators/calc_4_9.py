import streamlit as st
import pandas as pd
import math

def run_calc():
    st.subheader("⚡ 4-9. 다중 변압기 병렬운전: 부하분담 및 순환전류 분석")
    st.caption("변압기 간 %Z 차이에 따른 부하 분담과 전압비(Tap) 차이로 인한 무효 순환전류를 통합 시뮬레이션합니다.")

    # 1. 입력 섹션
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 병렬운전 변압기 설정")
        num_tr = st.slider("병렬운전 변압기 대수", 2, 5, 2)
        
        tr_data = []
        for i in range(num_tr):
            with st.expander(f"변압기 #{i+1} 사양 입력", expanded=(i < 2)):
                c1, c2, c3 = st.columns(3)
                capa = c1.number_input(f"용량(kVA)", min_value=100, value=1000, step=100, key=f"capa_{i}")
                imp = c2.number_input(f"%Z", min_value=1.0, value=6.0, step=0.1, key=f"imp_{i}")
                volt = c3.number_input(f"2차전압(V)", min_value=100, value=380, step=1, key=f"volt_{i}")
                tr_data.append({"id": i+1, "capa": capa, "imp": imp, "volt": volt})

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 운용 부하 조건")
        total_load = st.number_input("현재 총 부하 (kW)", min_value=0, value=1500)
        load_pf = st.slider("부하 역률 (cosφ)", 0.7, 1.0, 0.9, 0.05)
        
        btn = st.button("병렬운전 정밀 시뮬레이션 실행 🚀", type="primary", use_container_width=True)

    # 2. 결과 출력 섹션
    with col2:
        st.markdown("#### 🔍 통합 분석 보고서")
        if btn:
            total_kva = total_load / load_pf if load_pf > 0 else 0
            
            # [로직 1] 부하 분담 계산
            sum_s_over_z = sum(d['capa'] / d['imp'] for d in tr_data)
            
            # [로직 2] 순환전류 계산 (가장 전압이 높은 TR과 낮은 TR 간의 최대 순환전류 추정)
            v_list = [d['volt'] for d in tr_data]
            v_max, v_min = max(v_list), min(v_list)
            v_diff = v_max - v_min
            
            # 각 TR의 옴(Ohm) 임피던스 환산
            for d in tr_data:
                d['z_ohm'] = (d['imp'] / 100) * (d['volt']**2 / (d['capa'] * 1000))

            results = []
            for d in tr_data:
                share_kva = total_kva * (d['capa'] / d['imp']) / sum_s_over_z if sum_s_over_z > 0 else 0
                load_factor = (share_kva / d['capa']) * 100
                
                # 순환전류 영향 (단순화 모델: 평균 전압과의 차이에 의한 전류)
                v_avg = sum(v_list) / len(v_list)
                i_circ = abs(d['volt'] - v_avg) / d['z_ohm'] if d['z_ohm'] > 0 else 0
                
                results.append({
                    "변압기": f"TR-{d['id']}",
                    "분담 부하(kW)": round(share_kva * load_pf, 1),
                    "부하율(%)": round(load_factor, 1),
                    "예상 순환전류(A)": round(i_circ, 2),
                    "상태": "✅ 정상" if load_factor <= 100 else "🔥 과부하"
                })

            # 결과 테이블
            df = pd.DataFrame(results)
            st.dataframe(df, hide_index=True, use_container_width=True)

            st.markdown("---")
            st.markdown("##### 📍 실무 운영 진단")
            
            if v_diff > 0:
                st.warning(f"⚠️ **전압 불일치 발견:** 변압기 간 최대 **{v_diff}V**의 전압차가 존재합니다. 이로 인해 무부하 시에도 순환전류가 흐르며 변압기 온도 상승의 원인이 됩니다.")
            
            if any(r['부하율(%)'] > 100 for r in results):
                st.error("🚨 **용량 설계 주의:** 특정 변압기에 부하 쏠림 현상이 발생했습니다. %Z가 낮은 TR의 소손 위험이 있습니다.")
            else:
                st.success("✅ **운영 적정:** 현재 부하 분담 및 전압 편차가 허용 범위 내에 있습니다.")

            st.info("""
            1. **순환전류($I_c$):** 전압비가 다른 변압기를 병렬로 묶으면 전압이 높은 쪽에서 낮은 쪽으로 무효 전류가 흐릅니다. 이는 부하와 상관없이 변압기를 가열시킵니다.
            2. **%Z와 부하분담:** %Z가 작은 변압기일수록 자기 용량보다 더 많은 일을 하려 하므로, 증설 시에는 반드시 기존 TR과 %Z를 최대한 맞춰야 합니다.
            """)

            st.latex(r"I_c = \frac{\Delta V}{Z_A + Z_B}, \quad P_A = P_{total} \times \frac{S_A / \%Z_A}{\sum (S_i / \%Z_i)}")
            # 
        else:
            st.info("좌측에 변압기별 2차측 실측 전압과 사양을 입력하십시오.")