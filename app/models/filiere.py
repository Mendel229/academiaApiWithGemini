from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.base import Base
from sqlalchemy.sql import func

# SQLAlchemy Model
class FiliereDB(Base):
    __tablename__ = "filiere"

    id_filiere: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom_filiere: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    options_etude = relationship("OptionEtudeDB", back_populates="filiere")

# Pydantic Schemas
class FiliereBase(BaseModel):
    nom_filiere: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Base pour création uniquement
class FiliereBase(BaseModel):
    nom_filiere: str
    description: Optional[str] = None

# Pour création (requête)
class FiliereCreate(FiliereBase):
    pass

# Pour lecture (réponse)
class FiliereRead(FiliereBase):
    id_filiere: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

