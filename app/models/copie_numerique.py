from sqlalchemy import Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING, Dict
from pydantic import BaseModel, ConfigDict

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.etudiant import EtudiantDB
    from app.models.epreuve import EpreuveDB
    from app.models.reponse_eleve import ReponseEleveDB

# ----- Schémas Pydantic -----

class CopieNumeriqueBase(BaseModel):
    """
    Schéma de base pour une copie numérique.
    """
    id_etudiant: int
    id_epreuve: int
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CopieNumeriqueCreate(CopieNumeriqueBase):
    """
    Schéma pour la création d'une copie numérique.
    """
    pass

class CopieNumeriqueUpdate(CopieNumeriqueBase):
    """
    Schéma pour la mise à jour d'une copie numérique.
    """
    note_finale: Optional[float] = None
    statut: Optional[bool] = None

class CopieNumerique(CopieNumeriqueBase):
    """
    Schéma complet pour une copie numérique, incluant l'ID et les dates.
    """
    id_copie_numerique: int
    note_finale: Optional[float]
    statut: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----- Modèle SQLAlchemy -----

class CopieNumeriqueDB(Base):
    __tablename__ = "copie_numerique"

    id_copie_numerique: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_etudiant: Mapped[int] = mapped_column(ForeignKey("etudiant.id"), nullable=False)
    id_epreuve: Mapped[int] = mapped_column(ForeignKey("epreuve.id_epreuve"), nullable=False)

    note_finale: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    statut: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    etudiant: Mapped["EtudiantDB"] = relationship("EtudiantDB", back_populates="copies_numeriques")
    epreuve: Mapped["EpreuveDB"] = relationship("EpreuveDB", back_populates="copies_numeriques")

    reponses: Mapped[List["ReponseEleveDB"]] = relationship(
    "ReponseEleveDB", back_populates="copie_numerique", cascade="all, delete-orphan"
    )



class SoumissionCopieNumerique(BaseModel):
    id_etudiant: int
    id_epreuve: int
    reponses_qcm: Dict[int, str]       # id_question: réponse choisie
    reponses_code: List[str]           # Réponses dans l’ordre des questions code
    reponses_courtes: List[str]        # Réponses dans l’ordre des questions ouvertes


