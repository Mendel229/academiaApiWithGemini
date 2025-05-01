# app/models/epreuve.py
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, TYPE_CHECKING
from pydantic import BaseModel
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.question import QuestionDB


# ----- Schémas Pydantic -----

class EpreuveBase(BaseModel):
    titre: str
    duree: str
    niveau: str

class EpreuveCreate(EpreuveBase):
    pass

class Epreuve(EpreuveBase):
    id_epreuve: int

    model_config = {
        "from_attributes": True
    }


class EpreuveDB(Base):
    __tablename__ = "epreuve"

    id_epreuve: Mapped[int] = mapped_column(primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String, index=True)
    duree: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    niveau: Mapped[int] = mapped_column(String)

    questions: Mapped[List["QuestionDB"]] = relationship("QuestionDB", back_populates="epreuve")
