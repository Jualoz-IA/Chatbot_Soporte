# Chatbot de Soporte

Este proyecto es un chatbot de soporte desarrollado con Streamlit y varias integraciones de bases de datos y autenticación. A continuación se describen los componentes principales y cómo configurarlos.

## Estructura del proyecto

    ```
    CHATBOT_SOPORTE/
    ├── assets/
    │   ├── chat.drawio
    │   ├── Diagram.drawio
    │   ├── InitialDesign.drawio
    │   ├── ProyectRequeriments.txt
    │   └── roles.drawio
    ├── components/
    │   ├── chat.py
    │   ├── collectios.py
    │   ├── doc_gestion.py
    │   ├── options.py
    │   ├── parameters.py
    │   └── user_gestion.py
    ├── config/
    │   ├── agent/
    │   │   ├── IA_model.py
    │   │   ├── prompts.py
    │   │   └── RAG_Agent.py
    │   ├── database/
    │   │   ├── controllers/
    │   │   │   ├── collection_controller.py
    │   │   │   ├── login_controller.py
    │   │   │   ├── parametros_controller.py
    │   │   │   ├── qdrant_controller.py
    │   │   │   └── user_controller.py
    │   │   ├── init_bd.py
    │   │   ├── qdrant_gen_connection.py
    │   │   └── sql_connection.py
    │   └── models/
    │       ├── google_auth.py
    │       └── models_sql.py
    ├── login/
    │   └── login.py
    ├── .env
    ├── app.py
    └── requirements.txt
    ```

## Componentes principales

### components/

Esta carpeta contiene los módulos que gestionan la interfaz y la interacción con el chatbot:

- chat.py: Módulo principal del chatbot que maneja la interacción con el usuario, la recuperación de colecciones activas y la invocación del agente de RAG.
- collections.py: Interfaz para la gestión de colecciones en Qdrant, permitiendo crearlas, editarlas y eliminarlas desde Streamlit.
- doc_gestion.py: Permite la carga y procesamiento de documentos (TXT, CSV, PDF) para su almacenamiento en la base de datos vectorial.
- options.py: Administra las opciones de chat, permitiendo visualizar, modificar y cargar en bloque las opciones disponibles para los usuarios.
- parameters.py: Configuración de los parámetros del modelo de IA, como temperatura, cantidad máxima de tokens y penalizaciones.
- user_gestion.py: Gestión de usuarios, permitiendo listar, agregar, modificar y eliminar usuarios, además de visualizar estadísticas sobre roles.

### config/

Contiene los archivos de configuración de la base de datos, el modelo de IA y la autenticación:

- #### agent/

  - IA_model.py: Configura el modelo de IA, cargando parámetros desde la base de datos y estableciendo los valores para la generación de respuestas.
  - prompts.py: Contiene las plantillas de los prompts utilizados por el modelo de IA.
  - RAG_Agent.py: Implementa el agente RAG (Retrieval-Augmented Generation), encargado de gestionar la recuperación de información y la generación de respuestas.

- #### database/

  - init_bd.py: Inicializa la base de datos, creando tablas y usuarios por defecto.
  - sql_connection.py: Configura la conexión con PostgreSQL.
  - qdrant_gen_connection.py: Configura la conexión con Qdrant para el almacenamiento vectorial de documentos.

  - #### controllers/

    - collection_controller.py: Controlador para gestionar colecciones en Qdrant.
    - login_controller.py: Controlador para la autenticación y gestión de usuarios.
    - parametros_controller.py: Controlador para gestionar los parámetros del modelo.
    - qdrant_controller.py: Controlador para la conexión y manipulación de datos en Qdrant.
    - user_controller.py: Controlador para gestionar usuarios en la base de datos.

- #### models/

  - google_auth.py: Maneja la autenticación con Google mediante OAuth 2.0.
  - models_sql.py: Define los modelos SQLAlchemy para la base de datos.

### login/

- login.py: Módulo para el inicio de sesión de usuarios, soportando autenticación con credenciales y con Google OAuth.

### Otros archivos

- app.py: Archivo principal que inicia la aplicación, gestiona la autenticación y muestra la interfaz en Streamlit.
- requirements.txt: Lista de dependencias necesarias para el proyecto.
- .env: Archivo de configuración con variables de entorno, como credenciales de base de datos y claves de API.

## Requisitos Previos

Para ejecutar este proyecto, necesitarás tener instalado lo siguiente:
Software Base

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Gestor de bases de datos PostgreSQL
- Git (para clonar el repositorio)

## Servicios y Credenciales

- Credenciales de Google Cloud Platform para la autenticación
- Una instancia de Qdrant (ya sea local o en la nube)
- Acceso a una base de datos PostgreSQL
- Acceso y credenciales de Groq

## Variables de Entorno

Necesitarás configurar las siguientes variables de entorno en un archivo .env:

- Credenciales de base de datos
- Claves de API para servicios externos
- Configuración de Qdrant
- Configuración de Groq
- Credenciales de Google [docs](https://support.google.com/workspacemigrate/answer/9222992?hl=es-419)

## Espacio y Recursos

- Mínimo 4GB de RAM recomendado
- Al menos 1GB de espacio en disco para la instalación básica

## Instalación

Sigue estos pasos para configurar el entorno y ejecutar la aplicación:

1. Clona el repositorio:

Clona el repositorio desde

    ```bash
    git clone https://github.com/Jualoz-IA/Chatbot_Soporte.git
    cd Chatbot_Soporte
    ```

2. Crear y activar un entorno virtual

    ```bash
    python -m venv venv
    source venv/bin/activate  # En macOS y Linux
    venv\Scripts\activate  # En Windows
    ```

3. Instalar dependencias

    ```bash
    pip install -r requirements.txt
    ```

4. Configurar la base de datos PostgreSQL

Crea una base de datos en PostgreSQL y agrega las credenciales en el archivo .env.

    ```bash
    psql -U tu_usuario -d postgres -c "CREATE DATABASE chatbot_db;"
    ```

5. Configurar las variables de entorno

Crea un archivo .env en la raíz del proyecto con la siguiente estructura:

    ```bash
	GOOGLE_CLIENT_ID=TU_GOOGLE_CLIENT_ID
	GOOGLE_CLIENT_SECRET=TU_GOOGLE_CLIENT_SECRET
	GROQ_API_KEY=TU_GROQ_API_KEY
	DATABASE_URL=usuario:contraseña@localhost:5432/chatbot_db
	EMBEDDINGS_MODEL=distilbert-base-nli-stsb-mean-tokens
	QDRANT_DATABASE_URL=TU_QDRANT_URL
	QDRANT_API_KEY=TU_QDRANT_API_KEY
	USER=admin
	EMAIL=admin@example.com
	PASSWORD=admin123
    ```

6. Ejecutar la aplicación

    ```bash
    streamlit run app.py
    ```
