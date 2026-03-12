import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("🏗️ 6-11. DCIM 자산 배치 및 상면 하중 최적화 분석")
    st.caption("단위 면적당 랙(Rack) 무게를 계산하여 슬래브(Slab) 및 액세스 플로어의 구조적 안전성을 진단합니다.")

    # --- 상면 하중(Floor Loading) 기술 개요 ---
    with st.expander("📘 데이터센터 하중 설계 가이드", expanded=False):
        st.markdown("""
        **데이터센터 하중 관리**는 장비의 고밀도화에 따라 그 중요성이 커지고 있습니다.
        
        * **고정 하중(Dead Load)**: 건물 구조체, 액세스 플로어 등 자체 무게.
        * **활하중(Live Load)**: 서버 랙, UPS, 배터리 등 이동 및 실장 가능한 장비 무게.
        * **집중 하중(Point Load)**: 랙의 네 모서리(Leveling feet)에 집중되는 하중으로 액세스 플로어 판넬 강도와 직결됩니다.
        * **분포 하중(Distributed Load)**: 단위 면적($m^2$)당 가해지는 평균 하중으로 슬래브의 건전성을 결정합니다.
        """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 랙(Rack) 및 실장 데이터")
        rack_id = st.text_input("분석 대상 랙 ID", value="R-01-01")
        rack_weight = st.number_input("랙 자체 무게 (kg)", value=150, step=10)
        server_weight_total = st.number_input("실장 서버 총 무게 (kg)", value=600, step=50)
        
        st.markdown("---")
        st.markdown("#### 📏 2. 상면 점유 면적")
        # 표준 랙 규격(600mm x 1200mm) + 유지보수 공간 포함 면적
        occupancy_area = st.number_input("단위 랙당 점유 면적 ($m^2$)", value=1.2, step=0.1, 
                                         help="랙 규격 외에 전/후면 유지보수 통로 면적을 포함한 수치입니다.")

        st.markdown("---")
        st.markdown("#### 🏗️ 3. 바닥 구조 설계 기준")
        design_load_limit = st.number_input("바닥 설계 하중 ($kg/m^2$)", value=1200, step=100,
                                            help="데이터센터 표준 설계 하중은 보통 1,200 ~ 1,500 $kg/m^2$ 수준입니다.")

        btn = st.button("상면 하중 안전성 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {rack_id} 자산 배치 분석 리포트")
        if btn:
            # --- 분석 로직 ---
            total_weight = rack_weight + server_weight_total
            current_load_density = total_weight / occupancy_area
            safety_margin = design_load_limit - current_load_density
            load_ratio = (current_load_density / design_capa_load if 'design_capa_load' in locals() else (current_load_density / design_load_limit) * 100)

            # --- 판정 로직 ---
            if load_ratio > 100:
                l_status, l_color = "🚨 하중 초과 (Danger)", "red"
            elif load_ratio > 85:
                l_status, l_color = "⚠️ 한계 근접 (Warning)", "orange"
            else:
                l_status, l_color = "✅ 안전 (Safe)", "green"

            # 데이터프레임 구성 (열 너비 고정)
            res_data = {
                "분석 지표": ["총 실장 무게", "단위 면적당 하중", "설계 기준 대비", "안전 여유량"],
                "데이터": [f"{total_weight:,} kg", f"{current_load_density:.1f} $kg/m^2$", f"{load_ratio:.1f} %", f"{safety_margin:.1f} $kg/m^2$"],
                "진단 결과": ["측정값", "운용 분석", l_status, "확보됨" if safety_margin > 0 else "위험"]
            }
            
            st.dataframe(
                pd.DataFrame(res_data),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "분석 지표": st.column_config.TextColumn("분석 지표", width="medium"),
                    "데이터": st.column_config.TextColumn("데이터", width="small"),
                    "진단 결과": st.column_config.TextColumn("진단 결과", width="small")
                }
            )

            st.metric("상면 하중 이용률", f"{load_ratio:.1f} %", delta=f"{current_load_density - design_load_limit:.1f} $kg/m^2$", delta_color="inverse")

            st.markdown("---")
            st.markdown("##### 💡 전문가 상면 운영 제언")
            
            if load_ratio > 90:
                st.error(f"**[구조 안전 경고]** 단위 하중이 설계치의 90%를 초과했습니다. 추가 자산 실장을 금지하고, 필요시 하중 분산판(Spreader Plate) 설치를 검토하십시오.")
            
            st.info(f"""
            1. **집중 하중 주의:** 분포 하중({current_load_density:.1f} $kg/m^2$)이 정상이더라도, 랙의 다리 부분에 걸리는 **집중 하중**이 액세스 플로어 판넬의 국부 압축 강도를 초과하지 않는지 확인이 필요합니다.
            2. **고밀도 랙 배치:** 랙당 15kW 이상의 고밀도 서버 실장 시 무게가 1톤을 상회하는 경우가 많습니다. 슬래브 보강 구간에 우선 배치하는 전략이 필요합니다.
            3. **향후 확장성:** 현재 여유량({safety_margin:.1f} $kg/m^2$)을 고려하여 향후 스토리지 등 중량물 추가 도입 가능 여부를 DCIM 자산 맵에 기록해 두십시오.
            """)
            
            
        else:
            st.info("랙과 자산의 무게 정보를 입력하여 바닥 안전성을 시뮬레이션하십시오.")