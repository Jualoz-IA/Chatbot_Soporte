import streamlit as st
from config.agent.RAG_Agent import invoke

st.title('Chatbot')

# inicializa el historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# muestra el historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("What is up?")

if prompt:
    # muestra el input del usuario
    st.chat_message("user").markdown(prompt)
    # Agregar mensaje al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = invoke(prompt, st.session_state.messages)
    
    # mostrar la respuesta del modelo en el container de mensajes
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
        #response['source_documents']
    # Agregar respuesta del modelo al historial
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
