from langchain_groq import ChatGroq
import streamlit as st
import os

# Cargar las variables del archivo .env

# Obtener la clave API
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializar el modelo de Groq

@st.cache_resource
def load_model(model_name, temperature, api_key, max_tokens=100, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=None):
    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=api_key,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )

# Cargar el modelo con parámetros personalizados para inferencia
llm = load_model(
    model_name="gemma2-9b-it",  # Nombre del modelo a cargar.
    temperature=0.7,  # Controla la aleatoriedad de las respuestas. Valores más bajos hacen que las respuestas sean más deterministas.
    api_key="tu_api_key_aquí",  # La clave de API necesaria para acceder al modelo.
    max_tokens=150,  # Número máximo de tokens en la respuesta generada.
    top_p=0.9,  # Controla la probabilidad acumulada para la selección de tokens.
    frequency_penalty=0.5,  # Penalización para la repetición de tokens.
    presence_penalty=0.3,  # Penalización para la aparición de nuevos tokens.
)



import requests
import os

def get_models(api_key = groq_api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

