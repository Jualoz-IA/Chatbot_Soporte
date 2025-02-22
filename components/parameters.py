import streamlit as st
from sqlalchemy.orm import Session
from config.database.sql_connection import SessionLocal
from config.database.controllers.parametros_controller import guardar_parametros, get_parametros
from config.agent.IA_model import get_models

# Obtener modelos disponibles
models = get_models()
models_list = [modelo['id'] for modelo in models['data']]

# Conectar con la base de datos

__name__ = "__parameters__"

def parameters():
    db: Session = SessionLocal()

    # Interfaz en Streamlit
    st.title("Configuración del modelo")
    selected_model = st.selectbox("Modelos disponibles:", models_list)
    temperature = st.slider("Temperatura:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.slider("Máx Tokens:", min_value=1, max_value=2048, value=150, step=500)
    top_p = st.slider("Top-P:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    frequency_penalty = st.slider("Penalización Frecuencia:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    presence_penalty = st.slider("Penalización Presencia:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

    # Lista de parámetros a guardar
    parametros = [
        ("Modelo", selected_model, "string"),
        ("Temperatura", temperature, "float"),
        ("Max Tokens", max_tokens, "int"),
        ("Top-P", top_p, "float"),
        ("Penalización Frecuencia", frequency_penalty, "float"),
        ("Penalización Presencia", presence_penalty, "float"),
    ]

    # Botón para guardar parámetros
    if st.button("Guardar configuración"):
        guardar_parametros(db, parametros)
        st.success("Parámetros guardados correctamente")

    # Mostrar los parámetros guardados
    st.subheader("Parámetros guardados en la base de datos")
    parametros_db = get_parametros(db)
    st.table([{ "Clave": p.clave, "Valor": p.valor, "Tipo": p.tipo } for p in parametros_db])
    db.close()

if __name__ == "__parameters__":
    parameters()