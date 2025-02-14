import streamlit as st
from config.agent.RAG_Agent import rag_agent  # Importar el agente que creamos arriba

st.title('Chatbot')

# Mapeo de opciones a colecciones
COLLECTIONS_MAP = {
    "Debo hacer facturacion electronica": "Prueba de Fuego",
    "Que documentos necesito": "model",
    "Que requisitos tiene la facturacion electronica": "PRUEBA 2",
    "Cuales son los plazos de la facturacion electronica": "models",
    "Que beneficios tiene la facturacion electronica": "Task",
    "Penalidades y Sanciones": "newone",
    "Otro...": "resultscsv"
}

OPTIONS = list(COLLECTIONS_MAP.keys())

# Inicializa el historial si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Si no hay mensajes, muestra el mensaje de bienvenida del asistente
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(u"Hola, ¿Qué deseas hacer hoy?")
        # Muestra los botones de opciones
        for option in OPTIONS:
            if st.button(option, key=option, use_container_width=True):
                
                collection_name = COLLECTIONS_MAP[option]
                
                st.collection_name = collection_name
                # Agrega el mensaje del asistente al historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": u"Hola, ¿Qué deseas hacer hoy?"
                })
                # Agrega la selección como mensaje del usuario
                st.session_state.messages.append({
                    "role": "user",
                    "content": option
                })
                # Obtiene la respuesta usando la colección correcta
                response = rag_agent.invoke(question=option, chat_history=st.session_state.messages, collection=collection_name)

                # Agrega la respuesta del asistente
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"]
                })
                st.rerun()

# Si ya hay mensajes, muestra el historial
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input del chat para preguntas adicionales
if st.session_state.messages:
    prompt = st.chat_input("Escribe tu consulta")
    
    if prompt:
        default_collection = "facturacion_general"
        
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })

        response = rag_agent.invoke(question=prompt, chat_history=st.session_state.messages, collection=st.collection_name)
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response["answer"]
        })