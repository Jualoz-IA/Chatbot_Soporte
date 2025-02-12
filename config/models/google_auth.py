import streamlit as st
import requests
from urllib.parse import urlencode, parse_qs
import base64
import hashlib
import secrets
import http.server
import socketserver
from threading import Thread
from typing import Optional
import os

class GoogleOAuthHandler:
    def __init__(self):
        # Configuración de OAuth
        self.CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
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
