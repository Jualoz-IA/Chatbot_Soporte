import streamlit as st
from sqlalchemy.orm import Session
from config.database.sql_connection import SessionLocal
from config.database.controllers.parametros_controller import get_parametros
from langchain_groq import ChatGroq
import os

# Obtener la clave API
groq_api_key = os.getenv("GROQ_API_KEY")

# Conectar con la base de datos
db: Session = SessionLocal()

# Cargar los parámetros desde la base de datos
parametros_db = get_parametros(db)
parametros_dict = {p.clave: p.valor for p in parametros_db}

# Cerrar la sesión de base de datos
db.close()

# Función para cargar el modelo con los parámetros desde la base de datos
@st.cache_resource
def load_model():
    return ChatGroq(
        model=parametros_dict.get("Modelo", "gemma2-9b-it"),
        temperature=float(parametros_dict.get("Temperatura", 0.7)),
        api_key=groq_api_key,
        max_tokens=int(parametros_dict.get("Max Tokens", 150)),
        top_p=float(parametros_dict.get("Top-P", 0.9)),
        frequency_penalty=float(parametros_dict.get("Penalización Frecuencia", 0.5)),
        presence_penalty=float(parametros_dict.get("Penalización Presencia", 0.3)),
        stop=None
    )

# Inicializar el modelo LLM con los parámetros cargados
llm = load_model()
