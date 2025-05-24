from sqlalchemy import String, ForeignKey, Text, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel
from app.models.base import Base
from datetime import datetime

if TYPE_CHECKING:
    from app.models.epreuve import EpreuveDB
    from app.models.bonne_reponse import BonneReponseDB
    from app.models.reponse_eleve import ReponseEleveDB

# ----- Schémas Pydantic -----

class QuestionBase(BaseModel):
    type_question: str
    contenu: str
    option: Optional[List[str]] = None
    id_epreuve: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id_question: int
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

# ----- Modèle SQLAlchemy -----

class QuestionDB(Base):
    __tablename__ = "question"

    id_question: Mapped[int] = mapped_column(primary_key=True, index=True)
    type_question: Mapped[str] = mapped_column(String(50), nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    option: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    id_epreuve: Mapped[int] = mapped_column(ForeignKey("epreuve.id_epreuve"), nullable=False)

    # Relations
    epreuve: Mapped["EpreuveDB"] = relationship("EpreuveDB", back_populates="questions")
    bonnes_reponses: Mapped[List["BonneReponseDB"]] = relationship(
        "BonneReponseDB", back_populates="question", cascade="all, delete-orphan"
    )
    reponses_eleve: Mapped[List["ReponseEleveDB"]] = relationship(
        "ReponseEleveDB", back_populates="question", cascade="all, delete-orphan"
    )
