from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict
from app.models.professeur import ProfesseurDB
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.question import QuestionDB

# ----- Schémas Pydantic -----

class EpreuveBase(BaseModel):
    titre: str
    duree: str
    niveau: str
    created_at: datetime
    id_professeur: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class EpreuveCreate(EpreuveBase):
    pass

class Epreuve(EpreuveBase):
    id_epreuve: int

    model_config = ConfigDict(from_attributes=True)


class EpreuveDB(Base):
    __tablename__ = "epreuve"

    id_epreuve: Mapped[int] = mapped_column(primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String, index=True)
    duree: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    niveau: Mapped[str] = mapped_column(String, index=True)
    id_professeur: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("professeur.id"))

    questions: Mapped[List["QuestionDB"]] = relationship("QuestionDB", back_populates="epreuve")
    copies_numeriques = relationship("CopieNumeriqueDB", back_populates="epreuve")


# ----- Schémas Pydantic -----


class EpreuveTexte(BaseModel):
    texte_epreuve: str
    id_professeur: Optional[int]
