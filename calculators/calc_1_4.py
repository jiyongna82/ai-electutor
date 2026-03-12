import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-4. 전선관 굵기 선정 및 점유율 계산")
    st.caption("KEC 규정에 근거하여 전선관 내에 포설되는 전선의 총 단면적을 산출하고, 적정 전선관 규격을 자동으로 추천합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 전선관 및 전선 조건")
        
        # 전선관 종류 선택
        conduit_type = st.selectbox("전선관 종류", ["강제 전선관 (ST)", "합성수지관 (CD/HI-PVC)", "가요전선관 (GW/SF)"], index=0)
        
        # 전선 절연체 및 전압 정격
        wire_type = st.radio("전선 종류", ["IV/HIV (600V)", "F-CV/FR-8 (0.6/1kV)"], index=1, horizontal=True)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 포설 전선 구성")
        
        if 'conduit_wires' not in st.session_state:
            st.session_state.conduit_wires = [{"굵기(SQ)": 25.0, "가닥수": 3}]

        def add_wire():
            st.session_state.conduit_wires.append({"굵기(SQ)": 2.5, "가닥수": 0})

        new_wires = []
        for i, row in enumerate(st.session_state.conduit_wires):
            r1, r2 = st.columns(2)
            sq = r1.selectbox(f"전선 {i+1} 굵기 (SQ)", [2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240], index=5, key=f"sq_c_{i}")
            num = r2.number_input(f"전선 {i+1} 가닥수", min_value=0, value=int(row["가닥수"]), key=f"num_c_{i}")
            new_wires.append({"굵기(SQ)": sq, "가닥수": num})
        st.session_state.conduit_wires = new_wires

        st.button("➕ 전선 종류 추가", on_click=add_wire)
        
        limit_rate = st.slider("최대 허용 점유율 (%)", 32, 48, 40, 8, help="KEC 기준: 동일 굵기 48%, 서로 다른 굵기 40% 이하")

        btn = st.button("전선관 규격 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 전선관 설계 분석 결과")
        if btn:
            # 1. 전선 외경 데이터 (KS 규격 기반 근사치 데이터베이스)
            # {SQ: 외경(mm)} - 절연체 두께 포함
            WIRE_OD_DB = {
                2.5: 3.8, 4: 4.4, 6: 5.0, 10: 6.5, 16: 8.5, 25: 10.5, 
                35: 12.0, 50: 14.0, 70: 16.5, 95: 19.5, 120: 21.5, 
                150: 24.0, 185: 27.0, 240: 31.0
            }
            
            # 2. 전선 총 단면적 계산
            total_wire_area = 0
            for row in st.session_state.conduit_wires:
                od = WIRE_OD_DB.get(row["굵기(SQ)"], 0)
                area = (math.pi * (od**2) / 4) * row["가닥수"]
                total_wire_area += area
            
            # 3. 전선관 규격 매칭 (강제 전선관 호칭 기준 내경 mm)
            # {호칭: 내경(mm)}
            CONDUIT_SIZE_DB = {
                "16(1/2\")": 16.4, "22(3/4\")": 21.9, "28(1\")": 28.3, 
                "36(1-1/4\")": 36.9, "42(1-1/2\")": 43.1, "54(2\")": 54.8, 
                "70(2-1/2\")": 67.9, "82(3\")": 80.6, "92(3-1/2\")": 93.2, "104(4\")": 105.4
            }
            
            recommended_size = "규격 초과"
            current_fill_rate = 0.0
            
            for name, inner_id in CONDUIT_SIZE_DB.items():
                conduit_area = (math.pi * (inner_id**2) / 4)
                fill_rate = (total_wire_area / conduit_area) * 100
                if fill_rate <= limit_rate:
                    recommended_size = name
                    current_fill_rate = fill_rate
                    break
            
            # --- 결과 시각화 ---
            if recommended_size != "규격 초과":
                st.success(f"✅ 권장 전선관 규격: **{recommended_size}**")
                st.metric("현재 설계 점유율", f"{current_fill_rate:.2f} %", delta=f"{limit_rate - current_fill_rate:.1f}% 여유")
            else:
                st.error("❌ 전선관 규격을 초과하였습니다. 전선수를 줄이거나 케이블 트레이 방식을 검토하십시오.")

            st.write(f"- 전선 총 단면적: **{total_wire_area:.2f} mm²**")
            st.progress(min(current_fill_rate / 100, 1.0))

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **KEC 232.11 규정:** 서로 다른 굵기의 전선을 동일 전선관에 넣을 경우, 단면적 합계는 관 내단면적의 **40% 이하**여야 합니다.
            2. **굴곡 개소 주의:** 관로의 길이가 길거나 굴곡(Bend)이 많은 경우(3개소 초과), 인입 시 전선 피복 손상을 방지하기 위해 점유율을 **32% 이하**로 낮게 설계하는 것이 실무적으로 유리합니다.
            3. **데이터센터 유의사항:** DC 내의 전선관은 향후 증설이나 케이블 교체 가능성을 고려하여 여유 있는 규격을 선정하고, 전선관 끝단은 **부싱(Bushing)**을 사용하여 케이블 손상을 방지하십시오.
            """)
            
            st.latex(r"Fill \ Ratio \ (\%) = \frac{\sum (\text{Wire Area} \times \text{Count})}{\text{Conduit Inner Area}} \times 100")
            
        else:
            st.info("좌측에 포설할 전선의 규격과 가닥수를 입력해 주세요.")