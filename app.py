import streamlit as st
import importlib
from typing import List
from config.database.init_bd import init_db
from config.database.conectionsql import SessionLocal
from config.database.modelssql import User
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

def get_authorized_pages(roles: List[str]) -> dict:
    """Retorna las páginas autorizadas según los roles del usuario"""
    pages = {"chat": "ChatBot"}
    
    if "admin" in roles:
        pages.update({
            "collections": "Collections",
            "doc-gestion": "Documents Gestion",
            "parameters": "Models Parameters",
            "user-gestion": "User Gestion"
        })
    
    return pages

def show_page(page_name: str):
    """Carga dinámicamente el módulo de la página seleccionada"""
    try:
        module = importlib.import_module(f"components.{page_name}")
        module.main()  # Asegúrate de que cada módulo tenga una función main()
    except ModuleNotFoundError:
        st.error(f"No se encontró la página: {page_name}")

def init(roles: List[str]):
    """Inicializa la aplicación con la navegación entre páginas"""
    authorized_pages = get_authorized_pages(roles)

    # Mostrar las opciones de páginas autorizadas en la barra lateral
    selected_page = st.sidebar.selectbox(
        "Selecciona una página", 
        list(authorized_pages.values())
    )
    
    # Obtener la clave correspondiente al nombre de la página seleccionada
    selected_key = next(k for k, v in authorized_pages.items() if v == selected_page)

    # Mostrar la página seleccionada
    show_page(selected_key)

    # Cerrar sesión
    with st.sidebar:
        if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
            del st.session_state.user_id
            st.rerun()

def main():
    st.set_page_config(
        page_title="Chatbot",
        page_icon=":material/business_messages:",
    )

    init_db()
    is_authenticated, roles = check_if_authenticated()

    if not is_authenticated:
        if login.login():
            _, roles = check_if_authenticated()
            init(roles)
    else:
        init(roles)

if __name__ == "__main__":
    main()
