import streamlit as st
from config.agent.Gemma2_9b_it import load_model, get_models

models = get_models()
models_list = [modelo['id'] for modelo in models['data']]
st.title("Configuración del modelo")
currentGroqToken = st.text_input("Token groq actual:", "hola")
selected_model = st.selectbox("Modelos disponibles:", models_list)
temperature = st.slider("Selecciona la temperatura:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.slider("Selecciona el número máximo de tokens:", min_value=1, max_value=2048, value=150, step=500)
top_p = st.slider("Selecciona el top-p:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
frequency_penalty = st.slider("Selecciona la penalización por frecuencia:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
presence_penalty = st.slider("Selecciona la presencia por frecuencia:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)


