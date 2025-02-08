from langchain_groq import ChatGroq
import streamlit as st
import os

# Cargar las variables del archivo .env

# Obtener la clave API
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializar el modelo de Groq

@st.cache_resource
def load_model(model_name, temperature, api_key):
    return ChatGroq(model=model_name, temperature=temperature, api_key=api_key)

llm = load_model("gemma2-9b-it", 0.7, groq_api_key)

