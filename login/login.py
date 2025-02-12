# views/login.py
import streamlit as st
import webbrowser
from threading import Thread
import logging
import sys
from config.database.sql_connection import SessionLocal
from config.database.controllers import login_controller
from config.models.google_auth import GoogleOAuthHandler
import re
from config.models.models_sql import User

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def is_valid_email(email):
    """Verifica si el email tiene un formato válido."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$"
    return re.match(email_regex, email) is not None

def login_view():
    """Vista principal de login"""
    # Limpiar la barra lateral
    st.sidebar.empty()
    
    # Contenedor principal de login
    container = st.container(border=True)
    tab1, tab2 = container.tabs(["Crear Cuenta", "Iniciar Sesión"])

    with tab1:
        st.subheader("Crear cuenta")
        with st.form(key='crear_cuenta', border=False):
            username_input = st.text_input('UserName')
            email_input = st.text_input('Email')
            password_input = st.text_input('Contraseña', type='password')
            left, right = st.columns(2)

            submit_button = left.form_submit_button('Crear Cuenta', use_container_width=True)
            google_button = right.form_submit_button('Iniciar sesión con Google', use_container_width=True)

            if submit_button:
                handle_registration(username_input, email_input, password_input)
            elif google_button:
                handle_google_login()

    with tab2:
        st.subheader("Iniciar Sesión")
        with st.form(key='login', border=False):
            username_input = st.text_input('UserName')
            password_input = st.text_input('Contraseña', type='password')
            left, right = st.columns(2)
            
            login_button = left.form_submit_button('Iniciar Sesión', use_container_width=True)
            google_button = right.form_submit_button('Iniciar sesión con Google', type="primary", use_container_width=True)

            if login_button:
                handle_login(username_input, password_input)
            elif google_button:
                handle_google_login()

def handle_registration(username, email, password):
    """Maneja el proceso de registro de usuario"""
    if not username or not email or not password:
        st.error("Todos los campos son requeridos.")
        return
    
    if len(username) < 3 or len(username) > 15:
        st.error("El Username requiere entre 3 y 15 caracteres.")
        return
    
    if not is_valid_email(email):
        st.error("Por favor ingrese un email válido.")
        return
    
    db = SessionLocal()
    try:
        result = login_controller.create_user(db, username, email, password)
        
        if result["status"] == "success":
            st.session_state.user_id = result["user"]["id"]
            st.rerun()
        else:
            st.error(result["message"])
    finally:
        db.close()

def handle_login(username, password):
    """Maneja el proceso de inicio de sesión"""
    if not username or not password:
        st.error("Username y contraseña son requeridos.")
        return
    
    db = SessionLocal()
    try:
        result = login_controller.verify_user_credentials(db, username, password)
        
        if result["status"] == "success":
            st.session_state.user_id = result["user"]["id"]
            st.rerun()
        elif result["status"] == "user_not_found":
            st.error(f"El usuario '{username}' no existe.")
        elif result["status"] == "wrong_password":
            st.error("Contraseña incorrecta. Por favor intente nuevamente.")
        else:
            st.error("Ocurrió un error inesperado. Por favor intente nuevamente.")
    finally:
        db.close()

def handle_google_login():
    """Maneja el proceso de inicio de sesión con Google"""
    google_oauth = GoogleOAuthHandler()
    
    try:
        authorization_url = google_oauth.get_authorization_url()
        server_thread = google_oauth.start_local_server()
        
        if server_thread:
            webbrowser.open(authorization_url)
            server_thread.join(timeout=300)
            
            if google_oauth.authorization_code:
                tokens = google_oauth.exchange_code_for_token(google_oauth.authorization_code)
                
                if tokens and 'access_token' in tokens:
                    user_info = google_oauth.get_user_info(tokens['access_token'])
                    
                    if user_info:
                        process_google_user(user_info)
                    else:
                        st.error("No se pudo obtener la información del usuario")
                else:
                    st.error("No se pudo obtener el token de acceso")
            else:
                st.error("No se recibió código de autorización. Intente nuevamente.")
        else:
            st.error("No se pudo iniciar el servidor local para la autenticación.")
    except Exception as e:
        st.error(f"Error en la autenticación con Google: {str(e)}")

def process_google_user(user_info):
    """Procesa la información del usuario de Google"""
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == user_info['email']).first()
        
        if existing_user:
            st.session_state.user_id = existing_user.id
        else:
            base_username = user_info['name'].lower().replace(' ', '_')
            counter = 1
            while db.query(User).filter(User.username == base_username).first():
                base_username = f"{base_username}_{counter}"
                counter += 1
            
            result = login_controller.create_user(db, base_username, user_info['email'], None)
            
            if result["status"] == "success":
                st.session_state.user_id = result["user"]["id"]
        
        st.rerun()
    except Exception as e:
        st.error(f"Error al procesar usuario de Google: {str(e)}")
    finally:
        db.close()