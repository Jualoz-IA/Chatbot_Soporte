import streamlit as st
from config.database.conectionsql import init_db 
from login import login 
from components.user_gestion import user_gestion

# Crear páginas
chat_page = st.Page("components/chat.py", title="ChatBot", icon=":material/smart_toy:")
colletions_page = st.Page("components/collections.py", title="Collections", icon=":material/smart_toy:")
doc_gestion_page = st.Page("components/doc_gestion.py", title="Documents Gestion", icon=":material/ar_on_you:")
parameters_page = st.Page("components/parameters.py", title="Models Parameters", icon=":material/multiple_stop:")
user_gestion_page = st.Page("components/user_gestion.py", title="User Management", icon=":material/ar_on_you:")

st.set_page_config(page_title="Chatbot", page_icon=":material/business_messages:")

def check_if_authenticated():
    if "user_id" not in st.session_state:
        return False  # SIEMPRE RETORNA TRUE PORQUE EL LOGIN NO ESTÁ IMPLEMENTADO
    return True

def init():
    pg = st.navigation([
        chat_page, 
        colletions_page, 
        doc_gestion_page, 
        parameters_page, 
        user_gestion_page  # ⬅️ Se agregó aquí
    ])
    pg.run()

    if (pg.title == "User Management"):
        user_gestion()

def main():
    init_db()
    if not check_if_authenticated():
        # Si no está autenticado, mostramos el formulario de login
        if login.login():
            init()
    else:
        # Si está autenticado, mostramos las tareas
        init()

if __name__ == "__main__":
    main()
