import streamlit as st

# Crear páginas
chat_page = st.Page("components/chat/chat.py", title="ChatBot", icon=":material/smart_toy:")
colletions_page = st.Page("components/collections/collections.py", title="Collections", icon=":material/smart_toy:")
doc_gestion_page = st.Page("components/doc_gestion/doc-gestion.py", title="Documents Gestion", icon=":material/ar_on_you:")
parameters_page = st.Page("components/parameters/parameters.py", title="Models Parameters", icon=":material/multiple_stop:")
user_gestion_page = st.Page("components/user_gestion/user-gestion.py", title="User Gestion", icon=":material/ar_on_you:")
login_page = st.Page("components/login/login.py", title="Login", icon=":material/multiple_stop:") 

st.set_page_config(page_title="Chatbot", page_icon=":material/business_messages:")

if not st.session_state["HF_TOKEN"]:
    st.error("⚠️ Debes configurar tu token en la barra lateral antes de usar la aplicación.")
else:
    # Navegación
    pg = st.navigation([chat_page, colletions_page, doc_gestion_page, parameters_page, user_gestion_page, login_page])
    pg.run()