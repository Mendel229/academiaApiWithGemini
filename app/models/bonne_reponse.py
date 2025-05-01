from sqlalchemy import String, ForeignKey, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from app.models.base import Base
from datetime import datetime

if TYPE_CHECKING:
    from app.models.question import QuestionDB


# ----- Schémas Pydantic -----

class BonneReponseBase(BaseModel):
    bonne_reponse: str
    bareme: float = 1.0
    id_question: int

class BonneReponseCreate(BonneReponseBase):
    pass

class BonneReponse(BonneReponseBase):
    id_bonne_reponse: int
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# ----- Modèle SQLAlchemy -----

class BonneReponseDB(Base):
    __tablename__ = "bonne_reponse"

    id_bonne_reponse: Mapped[int] = mapped_column(primary_key=True, index=True)
    bonne_reponse: Mapped[str] = mapped_column(String, nullable=False)
    bareme: Mapped[float] = mapped_column(Numeric(5, 2), default=1.0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    id_question: Mapped[int] = mapped_column(ForeignKey("question.id_question"), nullable=False)

    # Relation vers la question
    question: Mapped["QuestionDB"] = relationship("QuestionDB", back_populates="bonnes_reponses")
