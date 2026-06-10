from fastapi import APIRouter


from app.models.chat_model import (
    ChatRequest
)


from app.services.rag_service import (
    ask_question
)



router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)



@router.post("")
def chat(
    request: ChatRequest
):

    answer = ask_question(
        request.question
    )


    return {
        "answer": answer
    }