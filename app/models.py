from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """Modelo para la petición de una pregunta."""
    question: str

class AnswerResponse(BaseModel):
    """Modelo para la respuesta del agente."""
    answer: str