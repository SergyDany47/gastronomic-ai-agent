import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

# --- Configuración Singleton ---
DB_PATH = Path(__file__).resolve().parent.parent / "restaurants.db"
DB = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# 👇 --- LÍNEA MODIFICADA --- 👇
# Actualizamos al modelo correcto que has encontrado en la documentación.
LLM = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Creación del agente por defecto.
AGENT_EXECUTOR = create_sql_agent(
    llm=LLM, 
    db=DB, 
    agent_type="openai-tools", 
    verbose=True
)

def get_agent_response(question: str) -> str:
    """
    Ejecuta el agente SQL con una pregunta y devuelve la respuesta.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        return "Error: La clave de API de Google no está configurada en el servidor."

    # Inyectamos nuestras reglas directamente en la pregunta del usuario.
    enhanced_question = f"""
    Pregunta del usuario: "{question}"
    
    ---
    Instrucciones Adicionales Obligatorias:
    1. Tu respuesta final DEBE ser siempre en español.
    ---
    """

    try:
        result = AGENT_EXECUTOR.invoke({"input": enhanced_question})
        return result.get("output", "No se pudo obtener una respuesta.")
    except Exception as e:
        print(f"Error en la ejecución del agente: {e}")
        return "Lo siento, ocurrió un error al procesar tu pregunta."