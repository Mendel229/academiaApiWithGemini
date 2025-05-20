from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from sqlalchemy.orm import Session

from app.models.question import Question, QuestionCreate
from app.services.question_service import QuestionService
from app.database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])

def create_response(success: bool, status: int, message):
    return JSONResponse(
        status_code=status,
        content={
            "success": success,
            "status": status,
            "message": message
        }
    )

@router.post("/", status_code=201)
async def creer_question(question_in: QuestionCreate, db: Session = Depends(get_db)):
    try:
        question_service = QuestionService(db)
        question = question_service.creer(question_in)
        return create_response(True, 201, jsonable_encoder(question))
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la création : {str(e)}")

@router.get("/")
async def lire_toutes_les_questions(db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    questions = question_service.lire_tous()
    return create_response(True, 200, jsonable_encoder(questions))

@router.get("/{id_question}")
async def lire_question(id_question: int, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    question = question_service.lire(id_question)
    if question is None:
        return create_response(False, 404, "Question non trouvée")
    return create_response(True, 200, jsonable_encoder(question))

@router.get("/showQuesByEp/{id_epreuve}")
async def get_quest_by_ep(id_epreuve: int, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    questions = question_service.get_quest_by_ep(id_epreuve)
    if questions is None:
        return create_response(False, 404, "Epreuve non trouvée")
    return create_response(True, 200, jsonable_encoder(questions))

@router.put("/{id_question}")
async def mettre_a_jour_question(id_question: int, question_in: QuestionCreate, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    question = question_service.mettre_a_jour(id_question, question_in)
    if question is None:
        return create_response(False, 404, "Question non trouvée")
    return create_response(True, 200, jsonable_encoder(question))

@router.delete("/{id_question}")
async def supprimer_question(id_question: int, db: Session = Depends(get_db)):
    try:
        question_service = QuestionService(db)
        question_service.supprimer(id_question)
        return create_response(True, 204, "Question supprimée avec succès")
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la suppression : {str(e)}")
