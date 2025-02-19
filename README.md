# Chatbot de Soporte

Este proyecto es un chatbot de soporte desarrollado con Streamlit y varias integraciones de bases de datos y autenticación. A continuación se describen los componentes principales y cómo configurarlos.

## Requisitos

- Python 3.8+
- Streamlit
- SQLAlchemy
- Otros paquetes especificados en `requirements.txt`

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/Chatbot_Soporte.git
    cd Chatbot_Soporte
    ```

2. Crea un entorno virtual y activa:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:
    Crea un archivo `.env` en la raíz del proyecto y añade las variables necesarias, por ejemplo:

    ```env
    DATABASE_URL=sqlite:///./test.db
    GOOGLE_CLIENT_ID=tu_google_client_id
    GOOGLE_CLIENT_SECRET=tu_google_client_secret
    QDRANT_DATABASE_URL=tu_url_de_qdrant
    QDRANT_API_KEY=tu_api_key_de_qdrant
    EMBEDDINGS_MODEL=nombre_del_modelo_de_embeddings
    USER=admin_username
    EMAIL=admin_email
    PASSWORD=admin_password
    ```

## Estructura del Proyecto

- `app.py`: Archivo principal que inicia la aplicación y maneja la autenticación.
- `login/login.py`: Maneja las vistas y lógica de autenticación.
- `components/parameters.py`: Configuración de parámetros del modelo.
- `components/collections.py`: Gestión de colecciones en Qdrant.
- `components/chat.py`: Interfaz del chatbot.
- `config/`: Configuraciones de base de datos y modelos.

## Uso

Para iniciar la aplicación, ejecuta:

```bash
  streamlit run app.py
```

## Descripción de Componentes

### `app.py`

Este archivo configura la aplicación principal de Streamlit, maneja la autenticación y la navegación entre diferentes páginas según los roles del usuario.

### `login/login.py`

Contiene la vista de login y la lógica para manejar el registro, inicio de sesión y autenticación con Google.

### `components/parameters.py`

Permite configurar los parámetros del modelo de IA utilizado por el chatbot.

### `components/collections.py`

Gestiona las colecciones en Qdrant, permitiendo crear, editar y eliminar colecciones.

### `components/chat.py`

Interfaz del chatbot donde los usuarios pueden interactuar con el asistente virtual.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.
