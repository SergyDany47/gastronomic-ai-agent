import os
from pathlib import Path
from dotenv import load_dotenv
import logging

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_agent_test():
    """
    Configura y ejecuta un bucle interactivo para probar el Agente SQL.
    """
    # --- 1. Carga de Variables de Entorno ---
    logging.info("Cargando variables de entorno...")
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ:
        logging.error("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
        return

    # --- 2. Conexión a la Base de Datos ---
    logging.info("Conectando a la base de datos SQLite...")
    db_path = Path(__file__).resolve().parent.parent / "restaurants.db"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    # --- 3. Configuración del Modelo de Lenguaje (LLM) ---
    logging.info("Configurando el modelo de lenguaje (Gemini)...")
    # Usamos temperature=0 para que el LLM sea lo más preciso y determinista posible
    # al generar las consultas SQL.
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    # --- 4. Creación del Agente SQL ---
    logging.info("Creando el Agente SQL...")
    # 'verbose=True' es MUY útil para depuración. Nos mostrará el "pensamiento"
    # del agente, incluyendo la consulta SQL que genera.
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    # --- 5. Bucle Interactivo de Preguntas ---
    print("\n✅ Agente SQL listo. Puedes empezar a hacer preguntas.")
    print("   Escribe 'salir' para terminar la sesión.\n")

    while True:
        try:
            user_question = input("Haz una pregunta: ")
            if user_question.lower() == 'salir':
                break
            
            # Invocamos al agente con la pregunta
            result = agent_executor.invoke({"input": user_question})
            
            # Imprimimos la respuesta final
            print("\nRespuesta del Agente:")
            print(result["output"])
            print("-" * 30)

        except Exception as e:
            logging.error(f"Ha ocurrido un error al procesar la pregunta: {e}")
            print("Lo siento, he encontrado un problema al procesar tu solicitud.")

if __name__ == "__main__":
    run_agent_test()