import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from typing import List

# Proyect imports
from config.database.init_bd import init_db
from config.database.conectionsql import SessionLocal
from config.database.modelssql import User
from components.user_gestion import user_gestion
from login import login



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

def get_user_info(user_id: int):
    """Obtiene la información del usuario desde la base de datos"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return {
                "username": user.username,
                "email": user.email,
                "roles": [role.name for role in user.roles]
            }
        return None
    finally:
        db.close()


def check_if_authenticated():
    """Verifica si el usuario está autenticado y obtiene sus roles"""
    if "user_id" not in st.session_state:
        return False, []

    roles = get_user_roles(st.session_state.user_id)
    return True, roles

def get_authorized_pages(roles: List[str]) -> List[st.Page]:
    """Retorna las páginas autorizadas según los roles del usuario"""
    chat_page = st.Page(
        "components/chat.py",
        title="ChatBot",
        icon=":material/smart_toy:"
    )
    collections_page = st.Page(
        "components/collections.py",
        title="Collections",
        icon=":material/smart_toy:"
    )
    doc_gestion_page = st.Page(
        "components/doc-gestion.py",
        title="Documents Gestion",
        icon=":material/ar_on_you:"
    )
    parameters_page = st.Page(
        "components/parameters.py",
        title="Models Parameters",
        icon=":material/multiple_stop:"
    )
    user_gestion_page = st.Page(
        "components/user_gestion.py",
        title="User Management",
        icon=":material/ar_on_you:"
    )

    authorized_pages = [chat_page]
    if "admin" in roles:
        authorized_pages.extend([
            collections_page,
            doc_gestion_page,
            parameters_page,
            user_gestion_page
        ])

    return authorized_pages

def init_auth(roles: List[str]):
    """Inicializa la aplicación con las páginas autorizadas"""
    authorized_pages = get_authorized_pages(roles)
    pg = st.navigation(authorized_pages)
    with st.sidebar:
        if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
            del st.session_state.user_id
            st.rerun()
    pg.run()
    if (pg.title == "User Management"):
        user_gestion()


def check_envs():
    # exit("DATABASE_URL: ")
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está definida en el archivo .env")
    print(f"DATABASE_URL: {DATABASE_URL}")
    exit("DATABASE_URL: " + DATABASE_URL)




def main():
    # streamlit stuff
    st.set_page_config(
        page_title="Chatbot",
        page_icon=":material/business_messages:",
    )

    # start database
    init_db()

    # start authentication
    is_authenticated, roles = check_if_authenticated()
    if not is_authenticated:
        if login.login():
            _, roles = check_if_authenticated()
            init_auth(roles)
    else:
        init_auth(roles)







if __name__ == "__main__":
    main()