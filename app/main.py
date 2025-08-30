from fastapi import FastAPI, HTTPException
from .models import QuestionRequest, AnswerResponse
from .agent_logic import get_agent_response

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Agente de Inteligencia Gastronómica",
    description="Una API para hacer preguntas en lenguaje natural sobre restaurantes de Madrid y Barcelona.",
    version="1.0.0"
)

@app.get("/", tags=["Status"])
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Bienvenido al Agente de Inteligencia Gastronómica"}

@app.post("/ask", response_model=AnswerResponse, tags=["Agent"])
def ask_agent(request: QuestionRequest):
    """
    Recibe una pregunta en lenguaje natural y devuelve la respuesta del agente SQL.
    """
    print(f"Pregunta recibida: {request.question}")
    if not request.question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    
    answer = get_agent_response(request.question)
    
    if "Error:" in answer or "Lo siento," in answer:
        raise HTTPException(status_code=500, detail=answer)
        
    return AnswerResponse(answer=answer)