import streamlit as st
from config.database.conectionsql import init_db 
from login import login 

# Crear páginas
chat_page = st.Page("components/chat.py", title="ChatBot", icon=":material/smart_toy:")
colletions_page = st.Page("components/collections.py", title="Collections", icon=":material/smart_toy:")
doc_gestion_page = st.Page("components/doc-gestion.py", title="Documents Gestion", icon=":material/ar_on_you:")
parameters_page = st.Page("components/parameters.py", title="Models Parameters", icon=":material/multiple_stop:")
user_gestion_page = st.Page("components/user-gestion.py", title="User Gestion", icon=":material/ar_on_you:")
st.set_page_config(page_title="Chatbot", page_icon=":material/business_messages:")

def check_if_authenticated():
    if "user_id" not in st.session_state:
        return False # SIEMPRE RETORNA TRUE PORQQUE EL LOGIN NO ESTA IMPLEMENTADO
    return True

def init():
    pg = st.navigation([chat_page, colletions_page, doc_gestion_page, parameters_page, user_gestion_page])
    pg.run()

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