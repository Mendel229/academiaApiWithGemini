# app/models/option_etude.py
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Pydantic Schemas
class OptionEtudeBase(BaseModel):
    nom_option: str
    id_filiere: int
    niveau: Optional[str] = None
    description: Optional[str] = None

class OptionEtudeCreate(OptionEtudeBase):
    pass

class OptionEtudeRead(OptionEtudeBase):
    id_option_etude: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# SQLAlchemy Model
class OptionEtudeDB(Base):
    __tablename__ = "option_etude"

    id_option_etude: Mapped[int] = mapped_column(primary_key=True)
    nom_option: Mapped[str] = mapped_column(String(255), nullable=False)
    id_filiere: Mapped[int] = mapped_column(Integer, ForeignKey("filiere.id_filiere"), nullable=False)
    niveau: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    filiere = relationship("FiliereDB", back_populates="options_etude")
    enseignements = relationship("EnseignementDB", back_populates="option_etude")

