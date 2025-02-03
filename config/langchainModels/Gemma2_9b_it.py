from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la clave API
groq_api_key = os.getenv('GROQ_API_KEY')

# Inicializar el modelo de Groq
llm = ChatGroq(model="gemma2-9b-it", temperature=0.7, api_key=groq_api_key)

# Definir el prompt
messages = [
    ("system", "Independientemente del idioma de la pregunta, siempre responde en español. No debes responder en ningún otro idioma."),
    ("human", "How does the aerodynamics of the F-35B work? And what are the differences between the different models?")
]

