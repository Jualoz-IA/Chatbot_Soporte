from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from typing import List

# Project imports
from config.database.init_bd import init_db
from config.database.sql_connection import SessionLocal
from config.models.models_sql import User
from login.login import login_view

def get_user_roles(user_id: int) -> List[str]:
    """Obtiene los roles del usuario desde la base de datos"""
    db = SessionLocal() 
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return [role.name for role in user.roles]
        return []
    finally:
        db.close()

def check_if_authenticated():
    """Verifica si el usuario está autenticado y obtiene sus roles"""
    return "user_id" in st.session_state, get_user_roles(st.session_state.get("user_id", None))

def get_authorized_pages(roles: List[str]) -> List[st.Page]:
    """Retorna las páginas autorizadas según los roles del usuario"""
    pages = {
        "chat": st.Page("components/chat.py", title="ChatBot", icon=":material/smart_toy:"),
        "collections": st.Page("components/collections.py", title="Collections", icon=":material/smart_toy:"),
        "doc_gestion": st.Page("components/doc_gestion.py", title="Documents Gestion", icon=":material/ar_on_you:"),
        "parameters": st.Page("components/parameters.py", title="Models Parameters", icon=":material/multiple_stop:"),
        "user_gestion": st.Page("components/user_gestion.py", title="User Management", icon=":material/ar_on_you:")
    }
    
    # Por defecto, todos los usuarios autenticados tienen acceso al chat
    authorized_pages = [pages["chat"]]
    
    # Páginas adicionales para administradores
    if "admin" in roles:
        authorized_pages.extend([
            pages["collections"],
            pages["doc_gestion"],
            pages["parameters"],
            pages["user_gestion"]
        ])
    
    return authorized_pages

def render_authenticated_view(roles: List[str]):
    """Renderiza la vista para usuarios autenticados"""
    authorized_pages = get_authorized_pages(roles)
    
    pg = st.navigation(authorized_pages)
    
    # Botón de cerrar sesión
    if st.sidebar.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
        # Limpiar todos los estados de la sesión
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    pg.run()



def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon=":material/business_messages:",
        initial_sidebar_state="collapsed"
    )

    # Ocultar el menú
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="collapsedControl"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    init_db()
    is_authenticated, roles = check_if_authenticated()

    if not is_authenticated:
        # Si no está autenticado, mostrar solo el login
        st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {display: none !important;}
            </style>
            """,
            unsafe_allow_html=True
        )
        login_view()
    else:
        render_authenticated_view(roles)

if __name__ == "__main__":
    main()