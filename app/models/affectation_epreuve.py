from sqlalchemy import DateTime, Integer, Date, Time, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base

class AffectationEpreuveDB(Base):
    __tablename__ = "affectation_epreuve"

    id_affectation_epreuve: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    id_session_examen: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("session_examen.id_session_examen", ondelete="CASCADE"),
        nullable=False
    )
    id_matiere: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("matiere.id_matiere", ondelete="RESTRICT"),
        nullable=False
    )
    id_option_etude: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("option_etude.id_option_etude", ondelete="RESTRICT"),
        nullable=False
    )
    id_professeur: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("professeur.id", ondelete="RESTRICT"),
        nullable=False
    )
    date_limite_soumission_prof: Mapped[Date] = mapped_column(Date, nullable=False)
    date_examen_etudiant: Mapped[Date] = mapped_column(Date, nullable=False)
    heure_debut_examen: Mapped[Time] = mapped_column(Time, nullable=False)
    duree_examen_prevue: Mapped[int] = mapped_column(Integer, nullable=False)
    id_epreuve: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("epreuve.id_epreuve", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )
    statut_affectation: Mapped[str] = mapped_column(String(50), nullable=False, server_default="assignee")
    commentaires_service_examens: Mapped[str | None] = mapped_column(Text, nullable=True)
    assigned_by: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("exam_service.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # relationships (optionnel si besoin d'accès)
    session_examen = relationship("SessionExamenDB", back_populates="affectations")
    matiere = relationship("MatiereDB", back_populates="affectations")
    option_etude = relationship("OptionEtudeDB", back_populates="affectations")
    professeur = relationship("ProfesseurDB", back_populates="affectations")
    epreuve = relationship("EpreuveDB", back_populates="affectation", uselist=False)
    assigner = relationship("ExamServiceDB", back_populates="affectations")

# Pydantic schemas
from pydantic import BaseModel, ConfigDict
from datetime import date, time

class AffectationEpreuveBase(BaseModel):
    id_session_examen: int
    id_matiere: int
    id_option_etude: int
    id_professeur: int
    date_limite_soumission_prof: date
    date_examen_etudiant: date
    heure_debut_examen: time
    duree_examen_prevue: int
    id_epreuve: int | None = None
    statut_affectation: str | None = None
    commentaires_service_examens: str | None = None
    assigned_by: int | None = None

class AffectationEpreuveCreate(AffectationEpreuveBase):
    pass

class AffectationEpreuveUpdate(BaseModel):
    id_session_examen: int | None = None
    id_matiere: int | None = None
    id_option_etude: int | None = None
    id_professeur: int | None = None
    date_limite_soumission_prof: date | None = None
    date_examen_etudiant: date | None = None
    heure_debut_examen: time | None = None
    duree_examen_prevue: int | None = None
    id_epreuve: int | None = None
    statut_affectation: str | None = None
    commentaires_service_examens: str | None = None
    assigned_by: int | None = None

class AffectationEpreuveRead(AffectationEpreuveBase):
    id_affectation_epreuve: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)