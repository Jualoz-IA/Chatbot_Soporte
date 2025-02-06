import streamlit as st
from config.agent.RAG_Agent import invoke

def main():
    st.title('Chatbot')

    # Inicializa el historial
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Muestra el historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What is up?")

    if prompt:
        # Muestra el input del usuario
        st.chat_message("user").markdown(prompt)
        # Agrega mensaje al historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = invoke(prompt, st.session_state.messages)
        
        # Muestra la respuesta del modelo en el container de mensajes
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
        
        # Agrega la respuesta del modelo al historial
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

if __name__ == "__main__":
    main()
