import streamlit as st
import requests
from urllib.parse import urlencode, parse_qs
import base64
import hashlib
import secrets
import webbrowser
import http.server
import socketserver
from threading import Thread
from typing import Optional
import logging
import sys
from config.database.conectionsql import SessionLocal
from config.database import functionssql

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

class GoogleOAuthHandler:
    def __init__(self):
        # Configuración de OAuth
        self.CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID")
        self.CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET")
        self.REDIRECT_PORT = 8505  # Puerto local para manejar callback
        self.REDIRECT_URI = f"http://localhost:{self.REDIRECT_PORT}"
        self.AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
        self.TOKEN_URL = "https://oauth2.googleapis.com/token"
        self.USER_INFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
        self.authorization_code: Optional[str] = None

        # Verificar que las credenciales estén configuradas
        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            st.error("Configuración de Google OAuth incompleta. Revise sus credenciales.")

    def generate_pkce_challenge(self):
        """Genera desafío PKCE para mayor seguridad."""
        verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().replace('=', '')
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().replace('=', '')
        return verifier, challenge

    def exchange_code_for_token(self, authorization_code):
        """Intercambia el código de autorización por un token de acceso."""
        # Verificar que el code_verifier exista en la sesión
        code_verifier = st.session_state.get('code_verifier')
        if not code_verifier:
            raise ValueError("No se encontró el code verifier. Reinicie el proceso de autenticación.")

        # Parámetros para el intercambio de token
        token_params = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URI,
            'code_verifier': code_verifier
        }

        try:
            # Solicitar token
            response = requests.post(self.TOKEN_URL, data=token_params)
            
            # Verificar respuesta
            if response.status_code != 200:
                st.error(f"Error en la solicitud de token: {response.text}")
                return None

            # Parsear respuesta
            tokens = response.json()
            return tokens
        except Exception as e:
            st.error(f"Error al intercambiar código: {str(e)}")
            return None

    def get_user_info(self, access_token):
        """Obtiene la información del usuario usando el token de acceso."""
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(self.USER_INFO_URL, headers=headers)
            
            if response.status_code != 200:
                st.error(f"Error al obtener información de usuario: {response.text}")
                return None

            return response.json()
        except Exception as e:
            st.error(f"Error al obtener información de usuario: {str(e)}")
            return None

    def start_local_server(self):
        """Inicia un servidor local para manejar el callback de Google."""
        class CallbackHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                # Extraer código de autorización de la URL
                try:
                    query_params = parse_qs(self.path.split('?')[1] if '?' in self.path else '')
                    logger.debug(f"Parámetros recibidos: {query_params}")
                    
                    if 'code' in query_params:
                        self.server.authorization_code = query_params['code'][0]
                    elif 'error' in query_params:
                        self.server.authorization_code = None
                    
                    # Respuesta al navegador
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<html><body><h1>Authentication Completed!</h1><p>You can close this window.</p></body></html>')
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
        
        # Crear un servidor socketserver personalizado
        class CallbackServer(socketserver.TCPServer):
            allow_reuse_address = True
            authorization_code = None

        # Iniciar servidor en un puerto específico
        try:
            httpd = CallbackServer(("", self.REDIRECT_PORT), CallbackHandler)
            
            def run_server():
                httpd.handle_request()  # Solo maneja una solicitud
                self.authorization_code = httpd.authorization_code

            # Iniciar servidor en un hilo separado
            server_thread = Thread(target=run_server)
            server_thread.start()
            return server_thread
        except Exception as e:
            st.error(f"No se pudo iniciar el servidor local: {e}")
            return None

    def get_authorization_url(self):
        """Genera la URL de autorización de Google."""
        # Generar desafío PKCE
        code_verifier, code_challenge = self.generate_pkce_challenge()
        
        # Guardar code_verifier en la sesión
        st.session_state.code_verifier = code_verifier

        # Parámetros para la solicitud de autorización
        params = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid email profile',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        # Construir URL de autorización
        authorization_url = f"{self.AUTHORIZATION_BASE_URL}?{urlencode(params)}"
        return authorization_url

def login_with_google(ubiq):
    """Maneja el flujo de inicio de sesión con Google."""
    google_oauth = GoogleOAuthHandler()

    # Verificación adicional de credenciales
    if not google_oauth.CLIENT_ID or not google_oauth.CLIENT_SECRET:
        st.error("Las credenciales de Google OAuth no están configuradas correctamente.")
        return

    # Botón para iniciar proceso de autenticación
    if ubiq.form_submit_button('Iniciar sesión con Google', use_container_width=True, type='primary'):
        try:
            # Generar URL de autorización
            authorization_url = google_oauth.get_authorization_url()
            
            # Iniciar servidor local para manejar callback
            server_thread = google_oauth.start_local_server()
            
            if server_thread:
                # Abrir URL de autorización en el navegador predeterminado
                webbrowser.open(authorization_url)
                
                # Esperar a que el servidor reciba el código de autorización
                server_thread.join(timeout=300)  # Esperar hasta 5 minutos
                
                if google_oauth.authorization_code:
                    # Intercambiar código por tokens
                    tokens = google_oauth.exchange_code_for_token(google_oauth.authorization_code)
                    
                    if tokens and 'access_token' in tokens:
                        # Obtener información del usuario
                        user_info = google_oauth.get_user_info(tokens['access_token'])
                        
                        if user_info:
                            # Crear o iniciar sesión con usuario
                            from config.database.conectionsql import SessionLocal
                            from config.database.modelssql import User
                            
                            db = SessionLocal()
                            try:
                                # Buscar usuario existente
                                existing_user = db.query(User).filter(User.email == user_info['email']).first()
                                
                                if existing_user:
                                    # Usuario ya existe
                                    st.session_state.user_id = existing_user.id
                                    st.success(f"Sesión iniciada como {existing_user.username}")
                                else:
                                    # Crear nuevo usuario
                                    base_username = user_info['name'].lower().replace(' ', '_')
                                    
                                    # Generar username único
                                    counter = 1
                                    while db.query(User).filter(User.username == base_username).first():
                                        base_username = f"{base_username}_{counter}"
                                        counter += 1
                               
                                    result = functionssql.create_user(db, base_username, user_info['email'], None)

                                st.rerun()
                            
                            except Exception as db_error:
                                st.error(f"Error en base de datos: {str(db_error)}")
                            finally:
                                db.close()
                        else:
                            st.error("No se pudo obtener la información del usuario")
                    else:
                        st.error("No se pudo obtener el token de acceso")
                else:
                    st.error("No se recibió código de autorización. Intente nuevamente.")
            else:
                st.error("No se pudo iniciar el servidor local para la autenticación.")
        
        except Exception as e:
            st.error(f"Error inesperado en la autenticación: {e}")

def login():
    container = st.container(border=True)
    
    tab1, tab2 = container.tabs(["Crear Cuenta", "Iniciar Sesión"])

    with tab1:
        st.subheader("Create Account")
        with st.form(key='Crear Cuenta', border=False):
            username_input = st.text_input('Enter UserName')
            email_input = st.text_input('Enter Email')
            password_input = st.text_input('Enter Password', type='password')
            left, right = st.columns(2)

            submit_button = left.form_submit_button('Crear Cuenta', use_container_width=True)
            login_with_google(right)

            if submit_button:
                # Validar que los campos no estén vacíos
                if not username_input or not email_input or not password_input:
                    st.error("All fields are required.")
                # Validar rango de longitud para el username
                elif len(username_input) < 3 or len(username_input) > 15:
                    st.error("Username must be between 3 and 15 characters long.")
                # Validar formato del email
                elif not is_valid_email(email_input):
                    st.error("Please enter a valid email address.")
                else:
                    db = SessionLocal()
                    result = functionssql.create_user(db, username_input, email_input, password_input)

                    if result["status"] == "error":
                        st.error(result["message"])  # Muestra el mensaje de error
                    elif result["status"] == "success":
                        user = result["user"]
                        st.success(f"Account created for {username_input} with email {email_input}!")
                    else:
                        st.error("Unexpected error occurred.")

    with tab2:
        st.subheader("Iniciar Sesión")
        with st.form(key='login', border=False):
            username_input = st.text_input('Enter UserName')
            password_input = st.text_input('Enter Password', type='password')
            left, right = st.columns(2)
            
            login_button = left.form_submit_button('Iniciar Sesión', use_container_width=True)
            login_with_google(right)


            if login_button:
                # Verificar si algún campo está vacío
                if not username_input or not password_input:
                    st.error("Both username and password are required.")
                else:
                    db = SessionLocal()
                    result = functionssql.verify_user_credentials(db, username_input, password_input)

                    if result["status"] == "user_not_found":
                        st.error(f"The username '{username_input}' does not exist.")
                    elif result["status"] == "wrong_password":
                        st.error("Incorrect password. Please try again.")
                    elif result["status"] == "success":
                        user = result["user"]
                        st.session_state.user_id = user["id"]  # Guardar el ID del usuario en la sesión
                        st.rerun()
                        return True
                    else:
                        st.error("An unexpected error occurred. Please try again.")
    
    return False

def is_valid_email(email):
    import re 
    """Verifica si el email tiene un formato válido."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$"
    return re.match(email_regex, email) is not None