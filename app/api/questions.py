from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.models.question import Question, QuestionCreate, QuestionDB  # Importe Question (Pydantic) et QuestionDB (SQLAlchemy)
from app.services.question_service import QuestionService
from app.database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=Question, status_code=201)
async def creer_question(question_in: QuestionCreate, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    return question_service.creer(question_in)

@router.get("/", response_model=List[Question])
async def lire_toutes_les_questions(db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    return question_service.lire_tous()

@router.get("/{id_question}", response_model=Question)
async def lire_question(id_question: int, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    question = question_service.lire(id_question)
    if question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return question

@router.put("/{id_question}", response_model=Question)
async def mettre_a_jour_question(id_question: int, question_in: QuestionCreate, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    question = question_service.mettre_a_jour(id_question, question_in)
    if question is None:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return question

@router.delete("/{id_question}", status_code=204)
async def supprimer_question(id_question: int, db: Session = Depends(get_db)):
    question_service = QuestionService(db)
    question_service.supprimer(id_question)
    return