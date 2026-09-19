import streamlit as st
import requests

st.set_page_config(
    page_title="Gym Telemetry & Performance",
    page_icon="🏋️‍♂️",
    layout="wide"
)

st.title("🏋️‍♂️ Gym Telemetry & Strength Performance Platform")
st.caption("Microservicio de Análisis de Cargas Máximas y Fuerza")

tab1 = st.tabs(["📊 Calculadora 1RM & Cargas"])[0]

with tab1:
    st.subheader("Análisis de Fuerza Máxima (1RM)")
    col1, col2 = st.columns(2)
    
    with col1:
        exercise = st.selectbox("Ejercicio", ["Press de Banca", "Sentadilla", "Peso Muerto", "Press Militar"])
        weight = st.number_input("Peso levantado (kg)", min_value=1.0, value=100.0, step=2.5)
        reps = st.number_input("Repeticiones realizadas", min_value=1, max_value=30, value=5)
        
        if st.button("Calcular 1RM y Zonas", type="primary"):
            payload = {"weight": weight, "reps": reps}
            try:
                response = requests.post("http://127.0.0.1:8001/api/v1/calculate-1rm", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["result_1rm"] = data["one_rm"]
                else:
                    st.error("Error al procesar con el microservicio")
            except Exception as e:
                st.error(f"Error de conexión con la API: {e}")

    with col2:
        if "result_1rm" in st.session_state:
            one_rm = st.session_state["result_1rm"]
            st.metric(label="Tu 1RM Estimado", value=f"{one_rm:.1f} kg")
            
            st.markdown("### Zonas de Carga Recomendadas")
            st.write(f"- 🔴 **Fuerza Máxima (90%)**: {one_rm * 0.90:.1f} kg (1-3 reps)")
            st.write(f"- 🟡 **Hipertrofia (75%)**: {one_rm * 0.75:.1f} kg (8-12 reps)")
            st.write(f"- 🟢 **Resistencia (60%)**: {one_rm * 0.60:.1f} kg (15+ reps)")