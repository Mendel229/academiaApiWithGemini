# app/models/matiere.py
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.base import Base


# Pydantic Schemas
class MatiereBase(BaseModel):
    nom_matiere: str
    description: Optional[str] = None

class MatiereCreate(MatiereBase):
    pass

class MatiereRead(MatiereBase):
    id_matiere: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# SQLAlchemy Model
class MatiereDB(Base):
    __tablename__ = "matiere"

    id_matiere: Mapped[int] = mapped_column(primary_key=True)
    nom_matiere: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    enseignements = relationship("EnseignementDB", back_populates="matiere")
