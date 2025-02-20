import streamlit as st
from sqlalchemy.orm import Session
from config.agent.RAG_Agent import rag_agent  # Importar el agente que creamos arriba
from config.database.sql_connection import SessionLocal
from config.database.controllers.collection_controller import get_active_collections_map, bulk_create_options

# Conectar con la base de datos
db: Session = SessionLocal()

def reset_chat():
    st.session_state.messages = []
    st.session_state.collection_name = "all_collection"

col1, col2 = st.columns([3,2], vertical_alignment='bottom')
with col1:
    st.title('Chatbot')
with col2:
    if st.button("🔄 Reiniciar Chat", type="tertiary", use_container_width=True):
        reset_chat()
        st.rerun()
        
collections_map = get_active_collections_map(db)

if "Otro..." not in collections_map:
    collections_map["Otro..."] = "all_collection"

OPTIONS = list(collections_map.keys())

# Inicializar el historial si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar la colección por defecto
if "collection_name" not in st.session_state:
    st.session_state.collection_name = "all_collection"

# Si no hay mensajes, muestra el mensaje de bienvenida del asistente
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(u"Hola, ¿Qué deseas hacer hoy?")
        # Muestra los botones de opciones
        for option in OPTIONS:
            if st.button(option, key=option, use_container_width=True):
                collection_name = collections_map[option]
                st.session_state.collection_name = collection_name
                st.session_state.messages.extend([
                    {
                        "role": "assistant",
                        "content": u"Hola, ¿Qué deseas hacer hoy?"
                    },
                    {
                        "role": "user",
                        "content": option
                    }
                ])
                
                # Obtener la respuesta usando la colección seleccionada
                response = rag_agent.invoke(
                    question=option, 
                    chat_history=st.session_state.messages, 
                    collection=collection_name
                )

                # Agregar la respuesta del asistente
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
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })

        # Usar la colección guardada en el estado de la sesión
        response = rag_agent.invoke(
            question=prompt, 
            chat_history=st.session_state.messages, 
            collection=st.session_state.collection_name
        )
        
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response["answer"]
        })