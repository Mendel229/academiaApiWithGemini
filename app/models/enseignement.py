# app/models/enseignement.py
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.base import Base

from app.models.professeur import ProfesseurDB
from app.models.matiere import MatiereDB
from app.models.option_etude import OptionEtudeDB

class EnseignementDB(Base):
    __tablename__ = "enseignement"

    id_enseignement: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_professeur:     Mapped[int] = mapped_column(Integer, ForeignKey("professeur.id"), nullable=False)
    id_matiere:        Mapped[int] = mapped_column(Integer, ForeignKey("matiere.id_matiere"), nullable=False)
    id_option_etude:   Mapped[int] = mapped_column(Integer, ForeignKey("option_etude.id_option_etude"), nullable=False)
    annee_academique:  Mapped[str] = mapped_column(String(255), nullable=False)
    created_at:        Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:        Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    professeur:   Mapped["ProfesseurDB"]   = relationship("ProfesseurDB", back_populates="enseignements")
    matiere:      Mapped["MatiereDB"]      = relationship("MatiereDB",    back_populates="enseignements")
    option_etude: Mapped["OptionEtudeDB"] = relationship("OptionEtudeDB", back_populates="enseignements")

# -- Pydantic schemas --
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EnseignementBase(BaseModel):
    id_professeur: int
    id_matiere: int
    id_option_etude: int
    annee_academique: str

class EnseignementCreate(EnseignementBase):
    pass

class EnseignementRead(EnseignementBase):
    id_enseignement: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
