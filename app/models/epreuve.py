from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.question import QuestionDB

# ----- Schémas Pydantic -----

class EpreuveBase(BaseModel):
    titre: str
    duree: Optional[str]  # Correction ici : rendre optionnel pour correspondre à la DB
    niveau: Optional[str]
    created_at: Optional[datetime] = None
    id_professeur: int

    model_config = ConfigDict(from_attributes=True)

class EpreuveCreate(EpreuveBase):
    pass

class Epreuve(EpreuveBase):
    id_epreuve: int

    model_config = ConfigDict(from_attributes=True)

class EpreuveTexte(BaseModel):
    texte_epreuve: str
    id_professeur: Optional[int]

# ----- Modèle SQLAlchemy -----

class EpreuveDB(Base):
    __tablename__ = "epreuve"

    id_epreuve: Mapped[int] = mapped_column(primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(Text, index=True)
    duree: Mapped[Optional[str]] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    niveau: Mapped[Optional[str]] = mapped_column(String, index=True)
    id_professeur: Mapped[int] = mapped_column(Integer, ForeignKey("professeur.id"), nullable=False)

    # Relations
    questions: Mapped[List["QuestionDB"]] = relationship("QuestionDB", back_populates="epreuve", cascade="all, delete")
    copies_numeriques = relationship("CopieNumeriqueDB", back_populates="epreuve", cascade="all, delete")
    

