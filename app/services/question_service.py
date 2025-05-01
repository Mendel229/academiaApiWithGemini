from sqlalchemy.orm import Session
from typing import List

from app.models.question import Question, QuestionCreate, QuestionDB

class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, question_in: QuestionCreate) -> Question:
        db_question = QuestionDB(**question_in.model_dump())
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return Question.from_orm(db_question)

    def lire(self, id_question: int) -> Question | None:
        question = self.db.query(QuestionDB).filter(QuestionDB.id_question == id_question).first()
        if question:
            return Question.from_orm(question)
        return None

    def lire_tous(self) -> List[Question]:
        questions = self.db.query(QuestionDB).all()
        return [Question.from_orm(question) for question in questions]

    def mettre_a_jour(self, id_question: int, question_in: QuestionCreate) -> Question | None:
        db_question = self.db.query(QuestionDB).filter(QuestionDB.id_question == id_question).first()
        if db_question:
            for field, value in question_in.model_dump().items():
                setattr(db_question, field, value)
            self.db.commit()
            self.db.refresh(db_question)
            return Question.from_orm(db_question)
        return None

    def supprimer(self, id_question: int):
        question = self.db.query(QuestionDB).filter(QuestionDB.id_question == id_question).first()
        if question:
            self.db.delete(question)
            self.db.commit()