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
            # 1. Cabeceras con la API Key requerida por FastAPI
            headers = {"X-API-Key": "sport-secure-key-2026"}
            
            # 2. Payload con los nombres de campos exactos del modelo Pydantic
            payload = {
                "exercise": exercise,
                "weight_kg": weight,
                "reps": reps
            }
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8001/api/v1/calculate-1rm", 
                    json=payload, 
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # 3. Mapeo correcto del campo devuelto por la API
                    st.session_state["result_1rm"] = data["estimated_1rm_kg"]
                    st.session_state["recommendation"] = data.get("recommendation", "")
                else:
                    st.error(f"Error {response.status_code}: Rechazado por la API")
            except Exception as e:
                st.error(f"Error de conexión con la API: {e}")

    with col2:
        if "result_1rm" in st.session_state:
            one_rm = st.session_state["result_1rm"]
            st.metric(label="Tu 1RM Estimado", value=f"{one_rm:.1f} kg")
            
            if "recommendation" in st.session_state:
                st.info(f"💡 {st.session_state['recommendation']}")
            
            st.markdown("### Zonas de Carga Recomendadas")
            st.write(f"- 🔴 **Fuerza Máxima (90%)**: {one_rm * 0.90:.1f} kg (1-3 reps)")
            st.write(f"- 🟡 **Hipertrofia (75%)**: {one_rm * 0.75:.1f} kg (8-12 reps)")
            st.write(f"- 🟢 **Resistencia (60%)**: {one_rm * 0.60:.1f} kg (15+ reps)")