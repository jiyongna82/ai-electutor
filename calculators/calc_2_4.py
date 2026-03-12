import streamlit as st
import math

def run_calc():
    st.subheader("⚖️ 2-4. 변압기 병렬운전(최대 5대) 부하 분담 분석")
    st.caption("최대 5대의 변압기를 병렬로 운전할 때, 각 TR의 용량과 %Z 차이에 따른 실제 부하 분담과 과부하 위험성을 정밀 진단합니다.")

    # 표준 정격 리스트
    TR_RATINGS = [0, 100, 200, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 5000, 7500, 10000]

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기별 제원 설정")
        st.info("💡 사용하지 않는 변압기는 용량을 '0'으로 설정하세요.")
        
        tr_data = []
        # 5대 입력을 위해 반복문 구성
        for i in range(1, 6):
            with st.expander(f"🔹 변압기 #{i} 설정", expanded=(i <= 2)):
                c1, c2 = st.columns(2)
                cap = c1.select_slider(f"용량 (kVA)", options=TR_RATINGS, value=(1000 if i <= 2 else 0), key=f"cap_{i}")
                z = c2.number_input(f"%Z (임피던스)", min_value=1.0, value=5.5, step=0.1, key=f"z_{i}")
                if cap > 0:
                    tr_data.append({"id": i, "cap": cap, "z": z, "term": cap / z})

        st.markdown("---")
        st.markdown("#### 🔌 2. 전체 부하 및 조건")
        
        total_installed_cap = sum([tr["cap"] for tr in tr_data])
        total_load_kw = st.number_input("현재 총 사용 부하 (kW)", min_value=0.0, value=float(total_installed_cap * 0.6), step=100.0)
        pf = st.slider("부하 역률 (%)", 70, 100, 95, 1)

        btn = st.button("5대 병렬 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 병렬운전 부하 분담 결과")
        if (btn or total_load_kw >= 0) and tr_data:
            cos_theta = pf / 100.0
            total_kva = total_load_kw / cos_theta if cos_theta > 0 else 0
            
            # 부하 분담 계산 핵심 (P_i = P_total * (C_i/%Z_i) / Σ(C_n/%Z_n))
            sum_term = sum([tr["term"] for tr in tr_data])
            
            st.write(f"총 피상 부하: **{total_kva:,.1f} kVA** / 총 설치 용량: **{total_installed_cap:,.0f} kVA**")
            
            overload_found = False
            results = []

            for tr in tr_data:
                share_kva = total_kva * (tr["term"] / sum_term)
                load_rate = (share_kva / tr["cap"]) * 100
                results.append({"id": tr["id"], "share": share_kva, "rate": load_rate})
                
                # 시각화
                st.markdown(f"**TR #{tr['id']} ({tr['cap']}kVA, {tr['z']}%Z)**")
                color = "red" if load_rate > 100 else "orange" if load_rate > 85 else "green"
                st.markdown(f"""
                    <div style="width:100%; background-color:#e0e0e0; border-radius:5px;">
                        <div style="width:{min(load_rate, 100)}%; background-color:{color}; height:20px; border-radius:5px;"></div>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"분담: **{share_kva:,.1f} kVA** (부하율: <span style='color:{color}; font-weight:bold;'>{load_rate:.1f}%</span>)", unsafe_allow_html=True)
                
                if load_rate > 100: overload_found = True

            st.divider()

            # --- 전문가 총평 ---
            if overload_found:
                st.error("🚨 **위험: 특정 변압기 과부하 감지!**")
                st.write("임피던스가 낮거나 용량이 상대적으로 작은 TR에 부하가 집중되고 있습니다. 즉시 부하를 조절하거나 뱅크 구성을 재검토하십시오.")
            else:
                # 임피던스 편차 체크
                zs = [tr["z"] for tr in tr_data]
                z_dev = (max(zs) - min(zs)) / min(zs) * 100
                if z_dev > 10:
                    st.warning(f"⚠️ **주의: 임피던스 편차 과다 ({z_dev:.1f}%)**")
                    st.write("변압기간 %Z 차이가 10%를 초과하여 부하 분담 균형이 깨져 있습니다. 장기 운전 시 특정 TR의 열화가 빨라집니다.")
                else:
                    st.success("✅ **정상: 5대 병렬 분담이 안정적입니다.**")

            # 뱅크 전체 한계 용량 계산
            # 각 TR이 100%가 되는 전체 부하 중 최솟값
            bank_limit = min([tr["cap"] * (sum_term / tr["term"]) for tr in tr_data])
            st.info(f"💡 **이 뱅크의 실제 한계 용량:** {bank_limit:,.1f} kVA")
            st.caption(f"(산술 합계 {total_installed_cap}kVA 대비 약 {total_installed_cap - bank_limit:,.1f}kVA 손실)")

        elif not tr_data:
            st.info("좌측에서 변압기 용량을 설정해주세요.")