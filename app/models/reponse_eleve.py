from sqlalchemy import Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.copie_numerique import CopieNumeriqueDB
    from app.models.question import QuestionDB

# ----- Schémas Pydantic -----

class ReponseEleveBase(BaseModel):
    id_copie_numerique: int
    id_question: int
    reponse_choisie: Optional[str] = None
    reponse_libre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ReponseEleveCreate(ReponseEleveBase):
    pass

class ReponseEleve(ReponseEleveBase):
    id_reponse_eleve: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----- Modèle SQLAlchemy -----

class ReponseEleveDB(Base):
    __tablename__ = "reponse_eleve"

    id_reponse_eleve: Mapped[int] = mapped_column(primary_key=True, index=True)
    reponse_choisie: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reponse_libre: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    id_copie_numerique: Mapped[int] = mapped_column(ForeignKey("copie_numerique.id_copie_numerique"), nullable=False)
    id_question: Mapped[int] = mapped_column(ForeignKey("question.id_question"), nullable=False)

    # Relations
    copie_numerique: Mapped["CopieNumeriqueDB"] = relationship(back_populates="reponses")
    question: Mapped["QuestionDB"] = relationship(back_populates="reponses_eleve")
